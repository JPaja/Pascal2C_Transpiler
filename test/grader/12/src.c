#include <stdio.h>
#include <string.h>


int main() {
int a[1005];
int n,i,max,x,br;
for(i=1;i<=1005;i++)
{
	a[i]=0;
};
scanf("%d", &n);
for(i=1;i<=n;i++)
{
	scanf("%d", &x);
	a[x]=(a[x] + 1);
};
max=-1;
for(i=1;i<=1005;i++)
{
	if((max < a[i]))
	{
		max=a[i];
		br=i;
	};
};
printf("%d%d%d", br, ' ', max);
return 0;
}