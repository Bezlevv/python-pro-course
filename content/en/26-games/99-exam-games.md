---
title: Exam: Games, Graphics, and GUI
summary: Final test for the module: pygame, Tkinter, PyQt6, Pillow, matplotlib, Kivy.
order: 99
duration: 30 min
difficulty: advanced
exam: true
---

<!--QUIZ-->
Which command starts the pygame game loop and keeps the window open?
- while running: with event handling
- pygame.loop()
- pygame.main()
* Correct answer: while running: with event handling
The game loop is a while-loop that runs until a pygame.QUIT event arrives.

What does pygame.key.get_pressed() do?
- Returns a list of all events for the frame
- Returns the state of all keys at the current moment
- Sets a press handler
* Correct answer: Returns the state of all keys at the current moment
get_pressed() returns the "live" keyboard state — convenient for continuous movement.

Which function checks a sprite's collision with a group and removes the hit sprites?
- pygame.sprite.spritecollide(player, balls, True)
- pygame.collide.group(player, balls)
- pygame.sprite.check(player, balls)
* Correct answer: pygame.sprite.spritecollide(player, balls, True)
The function returns a list of intersecting sprites, and True removes them from the group.

What does the mainloop() method do in Tkinter?
- Closes all windows
- Starts the event-handling loop
- Clears the screen
* Correct answer: Starts the event-handling loop
mainloop() keeps the window open, listens for events, and updates the interface.

How do you bind a Tkinter button to a function?
- Button(root, text="OK", command=my_func)
- Button(root, text="OK", action=my_func())
- Button(root, text="OK", on_click="my_func")
* Correct answer: Button(root, text="OK", command=my_func)
command takes a reference to the function without parentheses — it will be called when the button is pressed.

What does QTimer().start(1000) do in PyQt6?
- Starts a timer that fires every 1000 ms
- Stops the app after 1000 ms
- Waits 1000 ms and closes the window
* Correct answer: Starts a timer that fires every 1000 ms
QTimer emits a timeout signal every 1000 ms — convenient for animations and stopwatches.

What does QVBoxLayout do in PyQt6?
- Arranges widgets vertically from top to bottom
- Draws a border around the window
- Sets the window title
* Correct answer: Arranges widgets vertically from top to bottom
QVBoxLayout is a layout manager that stacks elements in a column.

Which Pillow method draws an oval (or circle)?
- draw.ellipse([x1, y1, x2, y2], fill="yellow")
- draw.oval([x1, y1, x2, y2])
- draw.circle([x1, y1, x2, y2])
* Correct answer: draw.ellipse([x1, y1, x2, y2], fill="yellow")
ellipse draws an oval inscribed in the given rectangle; equal sides produce a circle.

Which matplotlib function builds a bar chart?
- plt.bar(...)
- plt.plot(...)
- plt.scatter(...)
* Correct answer: plt.bar(...)
plt.bar takes labels and values and draws bars.

What does orientation="horizontal" mean for BoxLayout in Kivy?
- Widgets will be laid out in a row from left to right
- Widgets will be stacked in a column
- Widgets will overlap each other
* Correct answer: Widgets will be laid out in a row from left to right
Horizontal orientation places elements along a single line.
<!--/QUIZ-->
