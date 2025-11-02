# The Farmer Was Brainfucked

A simple-ish brainfuck interpreter for The Farmer Was Replaced changing `,` to read from the game and `.` to output a command

## Usage

Write your brainfuck code and minify it to a single string. I've included a minifier but there are many online.

Either `import the_farmer_was_brainfucked` and run `the_farmer_was_brainfucked(code)` or replace the `code` string with your own string and run the file.

## Write values

`till()` : 0  
`harvest()` : 1  
`move(Direction)`   : 4 + direction `{0:North,1:East,3:South,3:West}`  
`swap(Direction)`   : 32 + direction  
`use_item(Item)`    : 64 + item `{0:Items.Water,1:Items.Fertilizer,2:Items.Weird_Substance}`  
Generate ws*ws maze : 68  
`change_hat(Hat)`   : 69 + hat `{0:Hats.Straw_Hat,1:Dinosaur_Hat}`  
`plant(Entity)`     : 128 + plant `{0:Entities.Grass,1:Entities.Bush,2:Entities.Tree,3:Entities.Carrot,4:Entities.Pumpkin,5:Entities.Cactus,6:Entities.Sunflower}`  

## Read values

Read values depend on the plant under the drone.

First read is always a bitmask of water, entity, tilled state and harvestability: wwppppth  
Water is a number between 0 and 4 indicating 0-0.25, 0.25-0.5, 0.5-0.75 and 0.75-1

If the plant has companions second read is the number of the companion, third read is the X coordinate and fourth the Y coordinate

If the plant has a value (Cactus or Sunflower) second read is the center value, followed by North, East, South and West

If the plant is a pumpkin it returns a 1 byte ID. Values will be reused after 256 unique pumpkins measured.

When on an empty tilled field or apple second read will be a bitmask of available moves: (North=1, East=2, South=4, West=8)  
When on an apple this is followed by the X and Y coordinate of the next apple.

When on a hedge or chest return X and Y of the chest, followed by available moves.
