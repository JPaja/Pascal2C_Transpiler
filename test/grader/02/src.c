#include <stdio.h>
#include <string.h>


int main() {
int a,b;
scanf("%d%d", &a, &b);
printf("%d%d%d%d%d%d%d%d%d", (a + b), ' ', (a - b), ' ', (a * b), ' ', (a / b), ' ', (a % b));
return 0;
}