#include <stdio.h>
#include <string.h>

void check_arm(int,int,int,int);
void check_arm(int x,int cj,int cd,int cs)
{
	int arm;
	if((x < 0))
	{
		return ;
	};
	arm=(x == ((((cj * cj) * cj) + ((cd * cd) * cd)) + ((cs * cs) * cs)));
	if(arm)
	{
		printf("%s", "DA");
	}	else
	{
		printf("%s", "NE");
	};
}int main() {
int broj,cj,cd,cs;
scanf("None", &broj);
cj=(broj % 10);
cd=((broj / 10) % 10);
cs=((broj / 100) % 10);
check_arm(broj,cj,cd,cs);
return 0;
}