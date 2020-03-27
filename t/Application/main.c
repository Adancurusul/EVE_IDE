//Created at 2020-02-12 16:16:57
//Eve ide for gd32vf103

#include<stdio.h>
#include "gd32vf103_libopt.h"

void function_test(){

	prinf("hello");

	}
	

int main(){

	int a = 0;
	while (a<10)
	gpio_init(GPIOA, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_7);
		a++;

	function_test;
	}

	

	

	



