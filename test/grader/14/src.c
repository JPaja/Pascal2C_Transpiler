#include <stdio.h>
#include <string.h>


int main() {
int a[100];
int n,i,k;
scanf("%d%d", &n, &k);
for(i=1;i<=n;i++)
{
	scanf("%d", &a[i]);
};
for(i=k;i<=((n + k) - 1);i++)
{
	printf("%d%d", a[((i % n) + 1)], ' ');
};
return 0;
}