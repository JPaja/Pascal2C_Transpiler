#include <stdio.h>
#include <string.h>


int main() {
float a,b;
scanf("%f%f", &a, &b);
printf("%.2f%c%.2f%c%.2f", (a + b), ' ', (a - b), ' ', (a / b));
return 0;
}