#include <stdio.h>
#include <string.h>


int main() {
int a[100];
int i,n,max,tmax;
max=-32768;
tmax=0;
scanf("%d", &n);
for(i=1;i<=n;i++)
{
	scanf("%d", &a[i]);
};
for(i=1;i<=n;i++)
{
	tmax=(tmax + a[i]);
	if((tmax > max))
	{
		max=tmax;
	};
	if((tmax < 0))
	{
		tmax=0;
	};
};
printf("%d", max);
return 0;
}