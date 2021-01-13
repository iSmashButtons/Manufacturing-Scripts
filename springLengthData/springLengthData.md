# Spring Length data calculator.

## program goal

The goal of this program is to collect and retrieve the spring length for any SES part. The user should be prompted for a part number. If that number has been entered before, then the program should display the spring length. If the part number has not been entered before, then the program should take in data about the job: spring item number, and spring diameter (cavity center diameter). With that information, the program should figure out the spring series and then calculate the spring length. Then store that information for later use.

You will probably have to use a CSV to store the data.

In the future, if possible, use pygame to create an interface and allow assemblers to pick from different profiles, and input dimensions.

## Algorithm

1. ask user for drawing number (jacket detail)
2. look for that number in the CSV; if that drawing number exists, output the spring cut length.
3. if that drawing number does not exist ask the user for the following information:
    1. spring inventory code (500MS, or 302D, or 003x040x100, etc)
    2. spring diameter
4. If the spring is a series-500 or -600, calculate the length without adding the overlap. Otherwise, add the overlap.
5. if the spring is a helical, always add the overlap.
6. Write this new information to the CSV, and print to screen.

## Notes

Maybe use a dictionary to store seal spring info?

```python
spring={'partNo':'FH023370',
        'type':'helical',
        'Series':200,
        'overlap':0.040,
        'diameter':2.375,
        'length':7.501,
        'doubleSpring':'n',
        'innerDiameter':0,
        'outerDiameter':0}
```

### Some example spring data

- Drawing Number: FC01N13080J
- spring: 500MS ELGILOY
- spring diameter: 2.394
- spring cut-length: ?
- spring overlap:
