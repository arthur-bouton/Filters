# Recursive filters for C++ and Python


## C++


### Files

*filters.hh* and *filters2.hh* contain the template prototypes for low-pass first and second order recursive filters with different approximations (bilinear or homographic transforms, step or impulse response matching).

- ***filters.hh*** is to be used with the source file *filters.cc* in order to do separate compilation. In this case, the parameters have to be provided at instantiation time and parent filter templates cannot be instantiated (they are either abstracts or have a protected constructor).
- ***filters2.hh*** contains directly the full template definitions in order to embed the filters without requiring separate compilation. In this case, the filters need to be initialized explicitly after instantiation.


### Examples

The example below shows how to use a second order low-pass filter obtained by bilinear transformation with a sampling period of *T<sub>e</sub>=0.01* s, a natural frequency of *&omega;<sub>0</sub>=2&pi;* rad/s, a quality factor of *Q=0.7* and using separate compilation:

```
#include "cpp/filters.hh"

main()
{
	filters::LP_second_order_bilinear<double> filter( 0.01, 2*3.14, 0.7 );
	
	double input = 0;
	for ( int i = 0 ; i < 200 ; i++ )
	{
		if ( i > 10 )
			input = 1;

		filter.update( input );

		double output = filter.get_output();

		printf( "%f %f\n", input, output );
	}
}
```

If the filter parameters need to be initialized after the instantiation, in case of a class attribute for example, a smart pointer can be used:

```
#include "cpp/filters.hh"

main()
{
	filters::ptr_t<double> filter;

	filter = filters::ptr_t<double>( new filters::LP_second_order_bilinear<double>( 0.01, 2*3.14, 0.7 ) );
	
	double input = 0;
	for ( int i = 0 ; i < 200 ; i++ )
	{
		if ( i > 10 )
			input = 1;

		filter->update( input );

		double output = filter->get_output();

		printf( "%f %f\n", input, output );
	}


}
```

Otherwise, *filters2.hh* can be used:

```
#include "cpp/filters2.hh"

main()
{
	filters::LP_second_order<double> filter;

	filter.init_bilinear( 0.01, 2*3.14, 0.7 );
	
	double input = 0;
	for ( int i = 0 ; i < 200 ; i++ )
	{
		if ( i > 10 )
			input = 1;

		filter.update( input );

		double output = filter.get_output();

		printf( "%f %f\n", input, output );
	}
}
```


In any case, the input and output of the filter can be set with a pointer so that the values are changed directly when calling the method `update()` with no argument (a pointer must be used for the filter object though):

```
#include "cpp/filters.hh"

main()
{
	double input, output;

	auto filter = filters::ptr_t<double>( new filters::LP_second_order_bilinear<double>( 0.01, 2*3.14, 0.7, &input, &output ) );

	input = 0;
	for ( int i = 0 ; i < 200 ; i++ )
	{
		if ( i > 10 )
			input = 1;

		filter->update();

		printf( "%f %f\n", input, output );
	}
}
```

If the input and output point to the same variable, it provides a way of filtering this variable with minimal and non intrusive changes in the code:

```
#include "cpp/filters.hh"

main()
{
	double variable;

	auto filter = filters::ptr_t<double>( new filters::LP_second_order_bilinear<double>( 0.01, 2*3.14, 0.7, &variable, &variable ) );

	variable = 0;
	for ( int i = 0 ; i < 200 ; i++ )
	{
		if ( i > 10 )
			variable = 1;

		filter->update();

		printf( "%f\n", variable );
	}
}
```


These examples, once copied in a file *test.cc*, can be compiled with:<br />
`$ g++ -std=c++11 test.cc cpp/filters.cc -o test`<br />
Or if *filters2.hh* is used, there is no separate compilation:<br />
`$ g++ -std=c++11 test.cc -o test`

Then, with the *tracer* program available [here](https://github.com/Bouty92/Tracer "github.com/Bouty92/Tracer"), the result can be plotted directly with:<br />
`$ ./test | tracer`<br />
Or more sophisticatedly with:<br />
`$ ./test | tracer -L input,output -T '$T_e=0.01$ s        $\omega_0=2\pi$ rad/s        $Q=0.7$' -PS`<br />
Which gives the figure below:<br />
<p align="center">
	<img src="second_order_output.png?raw=true"
	title="Second order filter output">
</p>


## Python

To feed the filter, call its instance direclty. It can be given a single new value at a time, or a list of successive values at once:

```
from python.filters import *

input_list = [ 0 ]*10 + [ 1 ]*190

filter = LP_second_order( 0.01, 2*3.14, 0.7, transform='bilinear' )

output_list = filter( input_list )
```
