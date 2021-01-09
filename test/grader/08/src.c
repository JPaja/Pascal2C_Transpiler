#include <stdio.h>

bool jeProst(int n)
{
	int i;
	if((n <= 1))
	{
		return false;
	};
	for(i=(n / 2);i>=2;i--)
	{
		if(((n % i) == 0))
		{
			return false;
		};
	};
	return true;
}int main() {
int n,i,s;
scanf("%d", &n);
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
}while(false);
printf("%d\n", s);
return 0;
}