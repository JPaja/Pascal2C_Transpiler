#include <stdio.h>

int main() {
float a1,b1,a2,b2,p1,p2;
scanf("%d%d%d%d", &a1, &b1, &a2, &b2);
p1=((a1 * b1) / 2);
p2=((a2 * b2) / 2);
if((p1 > p2))
{
	printf("%d", '1');
}else
{
	if((p1 < p2))
	{
		printf("%d", '2');
	}	else
	{
		printf("%d", '0');
	};
};
return 0;
}