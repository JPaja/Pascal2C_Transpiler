#include <stdio.h>

char cifra_stotina(char s)
{
	if((s < 100))
	{
		return '0';
	}	else
	{
		return ('0' + (s / 100));
	};
}char cifra_desetica(char s)
{
	if((s < 10))
	{
		return '0';
	}	else
	{
		return ('0' + ((s / 10) % 10));
	};
}char cifra_jedinica(char s)
{
	return ('0' + (s % 10));
}int main() {
char s[100] = {0},t[100] = {0};
char ascii,tmp;
int i,j,len;
scanf("%d", &s);
i=1;
j=1;
len=length(s);
while((i <= len))
{
	ascii=s[i];
	i = i + 1;
	tmp=cifra_stotina(ascii);
	if((((tmp != '0') || (tmp == '0')) && (j > 1)))
	{
		t[j] = tmp;
		j = j + 1;
	};
	t[j] = cifra_desetica(ascii);
	j = j + 1;
	t[j] = cifra_jedinica(ascii);
	j = j + 1;
};
printf("%d", t);
return 0;
}