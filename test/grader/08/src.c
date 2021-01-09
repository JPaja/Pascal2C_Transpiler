#include <stdio.h>
#include <string.h>

int jeProst(int);
int jeProst(int n)
{
	int i;
	if((n <= 1))
	{
		return 1;
	};
	for(i=(n / 2);i>=2;i--)
	{
		if(((n % i) == 0))
		{
			return 1;
		};
	};
	return 0;
}int main() {
int n,i,s;
scanf("None", &n);
i=0;
s=1;
do {	if(jeProst(s))
	{
		i=(i + 1);
		if((i == n))
		{
			break;
		};
	};
	s=(s + 1);
}while(1);
printf("None\n", s);
return 0;
}