# Example:

	0; Bill: Hello!
		Hi!; goto 1
		Bye!; goto 2
	1; Bill: How are you?
		Good; goto 3
		Bad; goto 4
		Been worse; goto 5
	2; ...
	3; ...
	4; ...

# General Rule:

	[index(integer)]; [npc dialogue text]
		[player dialogue option]; [variable][+/-][integer] (optional); [(goto [index]) OR (end)]
		...
	...

## Conversation Node Indices
	index needs to follow 0, 1, 2, 3, ... without skipping

## Separations
	semicolons separate the sections of each entry
	newlines (<ENTER>) will break the line

## Variables
	this section is optional
	[varialbe] indicates the varialbe being editted
	[+/-] indicates addition or subtraction
	[integer] indicates the value to be added/subtracted

## Ignored
	whitespace is ignored everywhere except in [npc dialogue text] and [player dialogue option]
	capitalization is ognored everywhere except in [npc dialogue text] and [player dialogue option]
	
## Ends
	(end) indicates that you literally type "end", "END", or "EnD" or along those lines right there
	end indicates that the conversation is over and we pick another conversation from the baskets
	if no goto or end is indicated in the option, it will be assumed to be an endpoint
