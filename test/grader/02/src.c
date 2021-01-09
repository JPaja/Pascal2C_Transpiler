#include <stdio.h>
#include <string.h>


int main() {
int a,b;
scanf("%d%d", &a, &b);
printf("%d%c%d%c%d%c%d%c%d", (a + b), ' ', (a - b), ' ', (a * b), ' ', (a / b), ' ', (a % b));
return 0;
}