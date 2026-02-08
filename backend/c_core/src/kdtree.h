#ifndef KDTREE_H
#define KDTREE_H

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_LEN 256
#define MAX_TYPE_LEN 100
#define MAX_LINE_LEN 1024

// POI Structure
typedef struct {
  int id;
  char name[MAX_NAME_LEN];
  char type[MAX_TYPE_LEN];
  double lat;
  double lon;
} POI;

// KD-Tree Node
typedef struct Node {
  POI data;
  struct Node *left;
  struct Node *right;
} Node;

// Prototypes
Node *build_kdtree(POI *points, int n, int depth);
void range_search(Node *root, double lat, double lon, double radius_km,
                  const char *type_filter, const char *query);
void knn_search(Node *root, double lat, double lon, int k,
                const char *type_filter, const char *query);
void load_pois(const char *filename, POI **points, int *count);
void free_tree(Node *root);

#endif
