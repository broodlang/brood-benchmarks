/* Allocation / GC pressure. Build+walk a depth-12 tree n times.
 * Checksum = total nodes visited = n * (2^13 - 1).
 *
 * This is the row where C differs from every other column STRUCTURALLY, and the
 * difference is the point: the others allocate into a managed heap and let a
 * collector reclaim; C mallocs each node and frees it explicitly. So this measures
 * malloc/free against allocate/collect, which is a fair comparison of how each
 * language actually reclaims memory.
 *
 * What this deliberately does NOT do is bump-allocate the tree out of an arena and
 * drop it in one call. That is what a C programmer optimising this would really
 * write, and it would be several times faster — but it is a different program from
 * the one the other six run, and the suite's rule is same algorithm. A note for
 * anyone reading C's rank here: the arena version exists and is not in this column. */
#include "bench.h"

typedef struct Node {
    struct Node *l, *r;
} Node;

static Node *make(int d) {
    if (d == 0) return NULL;
    Node *node = malloc(sizeof *node);
    if (!node) exit(1);
    node->l = make(d - 1);
    node->r = make(d - 1);
    return node;
}

static long check(const Node *node) {
    return node ? 1 + check(node->l) + check(node->r) : 1;
}

static void release(Node *node) {
    if (!node) return;
    release(node->l);
    release(node->r);
    free(node);
}

int main(void) {
    long n = bench_n(200);
    const int DEPTH = 12;
    long total = 0;
    for (long i = 0; i < n; i++) {
        Node *t = make(DEPTH);
        total += check(t);
        release(t);
    }
    printf("%ld\n", total);
    return 0;
}
