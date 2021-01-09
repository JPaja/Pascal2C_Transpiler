#include <stdio.h>
#include <string.h>


int main() {
int i,j,n;
scanf("%d", &n);
for(i=n;i>=1;i--)
{
	for(j=(n - i);j>=1;j--)
	{
		printf("%c", ' ');
	};
	for(j=((2 * i) - 1);j>=1;j--)
	{
		printf("%c", '*');
	};
	printf("\n");
};
return 0;
}