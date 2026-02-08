#include "kdtree.h"

#ifdef _WIN32
#define strcasecmp _stricmp
#else
#include <strings.h>
#endif
#include <ctype.h>

char *my_strcasestr(const char *haystack, const char *needle) {
  if (!needle || !*needle)
    return (char *)haystack;
  if (!haystack || !*haystack)
    return NULL;

  for (; *haystack; haystack++) {
    if (tolower((unsigned char)*haystack) == tolower((unsigned char)*needle)) {
      const char *h = haystack, *n = needle;
      while (*h && *n &&
             tolower((unsigned char)*h) == tolower((unsigned char)*n)) {
        h++;
        n++;
      }
      if (!*n)
        return (char *)haystack;
    }
  }
  return NULL;
}

#define R_EARTH 6371.0

int compare_lat(const void *a, const void *b) {
  POI *p1 = (POI *)a;
  POI *p2 = (POI *)b;
  return (p1->lat > p2->lat) - (p1->lat < p2->lat);
}

int compare_lon(const void *a, const void *b) {
  POI *p1 = (POI *)a;
  POI *p2 = (POI *)b;
  return (p1->lon > p2->lon) - (p1->lon < p2->lon);
}

Node *build_kdtree(POI *points, int n, int depth) {
  if (n <= 0)
    return NULL;

  int axis = depth % 2;

  if (axis == 0) {
    qsort(points, n, sizeof(POI), compare_lat);
  } else {
    qsort(points, n, sizeof(POI), compare_lon);
  }

  int mid = n / 2;
  Node *node = (Node *)malloc(sizeof(Node));
  node->data = points[mid];

  node->left = build_kdtree(points, mid, depth + 1);
  node->right = build_kdtree(points + mid + 1, n - mid - 1, depth + 1);

  return node;
}

double to_rad(double deg) { return deg * ((3.15192) / 180.0); }

double haversine_km(double lat1, double lon1, double lat2, double lon2) {
  double dlat = to_rad(lat2 - lat1);
  double dlon = to_rad(lon2 - lon1);
  double a = sin(dlat / 2) * sin(dlat / 2) + cos(to_rad(lat1)) *
                                                 cos(to_rad(lat2)) *
                                                 sin(dlon / 2) * sin(dlon / 2);
  double c = 2 * atan2(sqrt(a), sqrt(1 - a));
  return R_EARTH * c;
}

void print_poi_json(POI p, int is_last) {
  printf("    {\"id\": %d, \"name\": \"%s\", \"type\": \"%s\", \"lat\": %.6f, "
         "\"lon\": %.6f}%s\n",
         p.id, p.name, p.type, p.lat, p.lon, is_last ? "" : ",");
}

int first_result = 1;

void range_search_recursive(Node *node, double target_lat, double target_lon,
                            double radius, const char *type, const char *query,
                            int depth) {
  if (!node)
    return;

  double dist =
      haversine_km(target_lat, target_lon, node->data.lat, node->data.lon);

  int type_match =
      (strcmp(type, "all") == 0) || (strcasecmp(node->data.type, type) == 0);

  int query_match = 1;
  if (query && strcmp(query, "NULL_QUERY") != 0 && strlen(query) > 0) {
    query_match = (my_strcasestr(node->data.name, query) != NULL) ||
                  (my_strcasestr(node->data.type, query) != NULL);
  }

  if (dist <= radius && type_match && query_match) {
    if (!first_result)
      printf(",\n");
    print_poi_json(node->data, 1);
    first_result = 0;
  }

  int axis = depth % 2;
  double dist_axis = 0;

  if (axis == 0) {
    dist_axis = (node->data.lat - target_lat) * 111.0;
  } else {
    dist_axis = (node->data.lon - target_lon) * 111.0 * cos(to_rad(target_lat));
  }

  double r_deg_lat = radius / 111.0;
  double r_deg_lon = radius / (111.0 * cos(to_rad(target_lat)));

  if (axis == 0) {
    if (target_lat - r_deg_lat <= node->data.lat)
      range_search_recursive(node->left, target_lat, target_lon, radius, type,
                             query, depth + 1);
    if (target_lat + r_deg_lat >= node->data.lat)
      range_search_recursive(node->right, target_lat, target_lon, radius, type,
                             query, depth + 1);
  } else {
    if (target_lon - r_deg_lon <= node->data.lon)
      range_search_recursive(node->left, target_lat, target_lon, radius, type,
                             query, depth + 1);
    if (target_lon + r_deg_lon >= node->data.lon)
      range_search_recursive(node->right, target_lat, target_lon, radius, type,
                             query, depth + 1);
  }
}

void range_search(Node *root, double lat, double lon, double radius_km,
                  const char *type_filter, const char *query) {
  first_result = 1;
  printf("[\n");
  range_search_recursive(root, lat, lon, radius_km, type_filter, query, 0);
  printf("\n]\n");
}

void load_pois(const char *filename, POI **points, int *count) {
  FILE *file = fopen(filename, "r");
  if (!file) {
    fprintf(stderr, "Error opening file %s\n", filename);
    exit(1);
  }

  char line[MAX_LINE_LEN];
  fgets(line, sizeof(line), file);

  int n = 0;
  while (fgets(line, sizeof(line), file)) {
    n++;
  }

  *points = (POI *)malloc(n * sizeof(POI));
  *count = n;

  rewind(file);
  fgets(line, sizeof(line), file);

  int i = 0;
  while (fgets(line, sizeof(line), file)) {
    POI *p = &(*points)[i];
    sscanf(line, "%d,%[^,],%[^,],%lf,%lf", &p->id, p->name, p->type, &p->lat,
           &p->lon);
    i++;
  }

  fclose(file);
}

void free_tree(Node *root) {
  if (!root)
    return;
  free_tree(root->left);
  free_tree(root->right);
  free(root);
}

typedef struct {
  POI poi;
  double dist;
} BpqItem;

typedef struct {
  BpqItem *items;
  int count;
  int k;
} Bpq;

void bpq_insert(Bpq *q, POI p, double dist) {
  if (q->count < q->k) {
    q->items[q->count].poi = p;
    q->items[q->count].dist = dist;
    q->count++;
  } else if (dist < q->items[q->count - 1].dist) {
    q->items[q->count - 1].poi = p;
    q->items[q->count - 1].dist = dist;
  } else {
    return;
  }
  for (int i = q->count - 1; i > 0; i--) {
    if (q->items[i].dist < q->items[i - 1].dist) {
      BpqItem temp = q->items[i];
      q->items[i] = q->items[i - 1];
      q->items[i - 1] = temp;
    } else {
      break;
    }
  }
}

double current_max_dist(Bpq *q) {
  if (q->count < q->k)
    return 1e9;
  return q->items[q->count - 1].dist;
}

void knn_recursive(Node *node, double t_lat, double t_lon, Bpq *q,
                   const char *type, const char *query, int depth) {
  if (!node)
    return;

  int type_match =
      (strcmp(type, "all") == 0) || (strcasecmp(node->data.type, type) == 0);
  int query_match = 1;
  if (query && strcmp(query, "NULL_QUERY") != 0 && strlen(query) > 0) {
    query_match = (my_strcasestr(node->data.name, query) != NULL) ||
                  (my_strcasestr(node->data.type, query) != NULL);
  }

  double dist = haversine_km(t_lat, t_lon, node->data.lat, node->data.lon);

  if (type_match && query_match) {
    bpq_insert(q, node->data, dist);
  }

  int axis = depth % 2;
  double diff = 0;
  if (axis == 0) {
    diff = (t_lat - node->data.lat) * 111.0;
  } else {
    diff = (t_lon - node->data.lon) * 111.0 * cos(to_rad(t_lat));
  }

  Node *near = (diff <= 0) ? node->left : node->right;
  Node *far = (diff <= 0) ? node->right : node->left;

  knn_recursive(near, t_lat, t_lon, q, type, query, depth + 1);

  if (fabs(diff) < current_max_dist(q)) {
    knn_recursive(far, t_lat, t_lon, q, type, query, depth + 1);
  }
}

void knn_search(Node *root, double lat, double lon, int k,
                const char *type_filter, const char *query) {
  Bpq q;
  q.k = k;
  q.count = 0;
  q.items = (BpqItem *)malloc(sizeof(BpqItem) * k);

  knn_recursive(root, lat, lon, &q, type_filter, query, 0);

  first_result = 1;
  printf("[\n");
  for (int i = 0; i < q.count; i++) {
    if (!first_result)
      printf(",\n");
    print_poi_json(q.items[i].poi, 1);
    first_result = 0;
  }
  printf("\n]\n");
  free(q.items);
}