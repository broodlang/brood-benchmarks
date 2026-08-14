/* Process startup + base memory. Prints 0, like every other port.
 * For C this is close to the floor of what the OS can do: exec, dynamic loader,
 * one write(2), exit. It is the reference the other `startup` numbers are read
 * against. */
#include "bench.h"

int main(void) {
    printf("0\n");
    return 0;
}
