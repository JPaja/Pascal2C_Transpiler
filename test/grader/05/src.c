#include <stdio.h>

int main() {
char c;
int lo,hi;
int d;
scanf("%d", &c);
lo=(c >= 'A');
hi=(c <= 'Z');
if((lo && hi))
{
	d=(c + 32);
}else
{
	d=(c - 32);
};
printf("%d", d);
return 0;
}