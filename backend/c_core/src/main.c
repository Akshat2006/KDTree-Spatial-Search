#include "kdtree.h"

int main(int argc, char *argv[]) {
  if (argc < 5 || argc > 7) {
    fprintf(stderr,
            "Usage: %s <lat> <lon> <type> <radius_or_k> [query] [mode]\n",
            argv[0]);
    return 1;
  }

  double target_lat = atof(argv[1]);
  double target_lon = atof(argv[2]);
  char *type = argv[3];
  double val = atof(argv[4]);

  char *query = "NULL_QUERY";
  if (argc >= 6) {
    query = argv[5];
  }

  char *mode = "radius";
  if (argc >= 7) {
    mode = argv[6];
  }

  POI *points = NULL;
  int n = 0;

  const char *datafile = "../data/pois.csv";
  FILE *f = fopen(datafile, "r");
  if (!f) {
    datafile = "c:/Users/HP/dsaelantigrav/backend/c_core/data/pois.csv";
  } else {
    fclose(f);
  }
  load_pois(datafile, &points, &n);

  POI *campus_points = NULL;
  int campus_n = 0;
  const char *campus_file = "../data/rv_university_campus.csv";
  f = fopen(campus_file, "r");
  if (!f) {
    campus_file = "c:/Users/HP/dsaelantigrav/backend/c_core/data/"
                  "rv_university_campus.csv";
  } else {
    fclose(f);
  }

  f = fopen(campus_file, "r");
  if (f) {
    fclose(f);
    load_pois(campus_file, &campus_points, &campus_n);

    if (campus_n > 0) {
      points = realloc(points, (n + campus_n) * sizeof(POI));
      memcpy(points + n, campus_points, campus_n * sizeof(POI));
      n += campus_n;
      free(campus_points);
    }
  }

  Node *root = build_kdtree(points, n, 0);

  if (strcmp(mode, "knn") == 0) {
    knn_search(root, target_lat, target_lon, (int)val, type, query);
  } else {
    range_search(root, target_lat, target_lon, val, type, query);
  }

  free_tree(root);
  free(points);

  return 0;
}
