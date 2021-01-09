#include <stdio.h>
#include <string.h>


int main() {
float a1,b1,a2,b2,p1,p2;
scanf("NoneNoneNoneNone", &a1, &b1, &a2, &b2);
p1=((a1 * b1) / 2);
p2=((a2 * b2) / 2);
if((p1 > p2))
{
	printf("%c", '1');
}else
{
	if((p1 < p2))
	{
		printf("%c", '2');
	}	else
	{
		printf("%c", '0');
	};
};
return 0;
}