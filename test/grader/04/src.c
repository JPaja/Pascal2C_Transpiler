#include <stdio.h>

void check_arm(int x,int cj,int cd,int cs)
{
	bool arm;
	if((x < 0))
	{
		return 0;
	};
	arm=(x == ((((cj * cj) * cj) + ((cd * cd) * cd)) + ((cs * cs) * cs)));
	if(arm)
	{
		printf("%d", 'DA');
	}	else
	{
		printf("%d", 'NE');
	};
}int main() {
int broj,cj,cd,cs;
scanf("%d", &broj);
cj=(broj % 10);
cd=((broj / 10) % 10);
cs=((broj / 100) % 10);
check_arm(broj,cj,cd,cs);
return 0;
}