#include <stdio.h>
#include <string.h>


int main() {
int niz[100];
int i,j,n,temp;
scanf("None", &n);
for(i=1;i<=n;i++)
{
	scanf("None", &niz[i]);
};
for(i=1;i<=n;i++)
{
	for(j=(i + 1);j<=n;j++)
	{
		if((niz[i] <= niz[j]))
		{
			continue;
		}		else
		{
			temp=niz[i];
			niz[i]=niz[j];
			niz[j]=temp;
		};
	};
};
for(i=1;i<=n;i++)
{
	printf("None%c", niz[i], ' ');
};
return 0;
}