#include <m8c.h>        // part specific constants and macros
#include "PSoCAPI.h"    // PSoC API definitions for all User Modules
#include <stdio.h>
#include <string.h>

// define states
typedef enum
{
PARSE_STATE_INIT,
	PARSE_STATE_WIFI,
	PARSE_STATE_LAT,
	PARSE_STATE_LONG
} states;

void main(void)
{	
int str_ptr;
	char wifi_str[32];
	char lat[32];
	char lon[32];
	char newchar;
	
	states state = PARSE_STATE_INIT;     // set to initial state
	M8C_EnableGInt;      
   	Counter8_1_Start();       
    	LCD_1_Start();
	RX8_1_Start(RX8_1_PARITY_NONE);
	
	while (1)
	{	
		newchar = RX8_1_cGetChar();     // read character
		if (newchar == ';')
		{
			state = PARSE_STATE_WIFI;     // move to next state
			str_ptr = 0;     // reset string pointer
		}
		else
		{
			switch (state)
			{
				case (PARSE_STATE_INIT):
					if (newchar == ';')
					{
						state = PARSE_STATE_WIFI;
						str_ptr = 0;
					}
					break;
				case (PARSE_STATE_WIFI):     // print signal strength
					if (newchar != ':')
						// put character in string
						wifi_str[str_ptr++] = newchar;
					else
					{
						// print string and label
						wifi_str[str_ptr++]='\0';
						state = PARSE_STATE_LAT;
						LCD_1_Position(0,0);
						LCD_1_PrCString("dBm");
						LCD_1_Position(1,0);
						LCD_1_PrString(wifi_str);
						str_ptr = 0;
					}
					break;
				case (PARSE_STATE_LAT):     // print latitude
					if (newchar != '!')
						lat[str_ptr++] = newchar;
					else
					{
						lat[str_ptr++]='\0';
						state = PARSE_STATE_LONG;
						LCD_1_Position(0,4);
						LCD_1_PrCString("A");
						LCD_1_Position(0,5);
						LCD_1_PrString(lat);
						str_ptr = 0;
					}
					break;
				case (PARSE_STATE_LONG):     // print longitude
					if (newchar != '#')
						lon[str_ptr++] = newchar;
					else		
					{
						lon[str_ptr++]='\0';
						state = PARSE_STATE_INIT;
						LCD_1_Position(1,4);
						LCD_1_PrCString("O");
						LCD_1_Position(1,5);
						LCD_1_PrString(lon);
						str_ptr = 0;
					}
					break;
				
			}
		}
	}
}
