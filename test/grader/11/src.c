#include <stdio.h>
#include <string.h>


int main() {
int a[100],b[100],c[100];
int n,ai,bi,ci,i;
bi=1;
ci=1;
scanf("%d", &n);
for(ai=1;ai<=n;ai++)
{
	scanf("%d", &a[ai]);
};
for(ai=1;ai<=n;ai++)
{
	if(((a[ai] % 2) == 0))
	{
		b[bi]=a[ai];
		bi=(bi + 1);
	}	else
	{
		c[ci]=a[ai];
		ci=(ci + 1);
	};
};
for(i=1;i<=(bi - 1);i++)
{
	printf("%d%d", b[i], ' ');
};
printf("\n");
for(i=1;i<=(ci - 1);i++)
{
	printf("%d%d", c[i], ' ');
};
return 0;
}