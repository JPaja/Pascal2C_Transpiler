#include <stdio.h>

int main() {
int i,j,n;
scanf("%d", &n);
for(i=n;i>=1;i--)
{
	for(j=(n - i);j>=1;j--)
	{
		printf("%d", ' ');
	};
	for(j=((2 * i) - 1);j>=1;j--)
	{
		printf("%d", '*');
	};
	printf("\n");
};
return 0;
}