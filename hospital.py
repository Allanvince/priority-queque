import pygame
import heapq
import tkinter as tk
from tkinter import messagebox
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 650
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 69, 0)
BORDER_THICKNESS = 2
FONT_SIZE = 24
PADDING = 20
BUTTON_WIDTH = 200
MAX_PATIENTS = 20

font_family = "Gabriola"

patient_counter = 1

# Priority Queue
priority_queue = []

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hospital Priority Queue")
font = pygame.font.Font(pygame.font.match_font(font_family), FONT_SIZE)

# Function to render text
def draw_text(text, rect, color=BLACK):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery))
    screen.blit(text_surface, text_rect)

# Function to draw the priority queue on the screen
def draw_priority_queue():
    display_rect = pygame.Rect(WIDTH // 2 + 25, display_margin_top, display_width, display_height)
    gap_between_items = 4  # Adjust this value as needed

    # Sort the priority queue based on age and order of addition
    sorted_queue = sorted(priority_queue, key=lambda x: (x[1], x[0]))

    for i, (_, patient_id, patient) in enumerate(sorted_queue):
        if i == 0:
            y_position = display_rect.top + 12
        else:
            y_position = display_rect.top + 12 + i * (FONT_SIZE + gap_between_items)

        text = f"{i + 1}. {patient['name']} - Age: {patient['age']}"
        text_surface = font.render(text, True, BLACK)

        # Check if the text fits within the display area
        if display_rect.collidepoint(display_rect.centerx, y_position):
            text_rect = text_surface.get_rect(center=(display_rect.centerx, y_position))
            screen.blit(text_surface, text_rect)

            # Load and render an image with reduced size
            image_path = "C:/Users/user/Desktop/repos/hospital-priority-queue/scout.png"
            if os.path.exists(image_path):
                original_image = pygame.image.load(image_path)
                # Define the desired width and height for the image
                desired_width, desired_height = 30, 30  # Adjust these values as needed
                # Scale the image to fit the desired size
                scaled_image = pygame.transform.scale(original_image, (desired_width, desired_height))
                # Calculate the position to center the image next to the text
                image_x = display_rect.centerx + text_rect.width // 2 + PADDING
                image_y = y_position - scaled_image.get_height() // 2
                # Blit the scaled image onto the screen
                screen.blit(scaled_image, (image_x, image_y))

        else:
            break

# Function to check if the mouse is over a button
def is_button_clicked(pos, button_rect):
    return button_rect.collidepoint(pos)

# Keep track of patient numbers
def update_patient_numbers():
    global added_patients
    for i, (_, patient_id, patient) in enumerate(priority_queue):
        priority_queue[i] = (patient['age'], i + 1, patient)
    added_patients = len(priority_queue)

# Function to check if the mouse is over an input area
def is_input_area_hovered(pos, input_rect):
    return input_rect.collidepoint(pos)

# Tkinter setup for error alert
root = tk.Tk()
root.withdraw()

# Function to show an alert error
def show_error(message):
    messagebox.showinfo("Error", message)

def show_max_capacity_error():
    messagebox.showinfo("Error", "Max capacity reached. Cannot add more patients.")

# Function to display length of the priority queue
def show_queue_length():
    length = len(priority_queue)
    messagebox.showinfo("Priority Queue Length", f"The length of the priority queue is {length}.")

# Function to add a patient to the priority queue
def add_patient(patient_name, patient_age):
    global added_patients, patient_counter
    patient = {'name': patient_name, 'age': patient_age}
    heapq.heappush(priority_queue, (patient['age'], patient_counter, patient))
    update_patient_numbers()
    added_patients = len(priority_queue)
    patient_counter += 1

# Function to check if the priority queue is empty
def check_empty():
    is_empty = not bool(priority_queue)
    messagebox.showinfo("Priority Queue Is Empty", f"The priority queue is {'empty' if is_empty else 'not empty'}.")

# Function to peek at the patient at the top of the priority queue
def peek_at_top():
    if priority_queue:
        age, _, patient = priority_queue[0]
        messagebox.showinfo("Top", f"Name: {patient['name']}\nAge: {patient['age']}")
    else:
        messagebox.showinfo("Top", "The priority queue is empty.")

# Initialize input fields and labels
name_label_rect = pygame.Rect(PADDING, PADDING, BUTTON_WIDTH, 30)
name_input_rect = pygame.Rect(name_label_rect.left, name_label_rect.bottom + 5, BUTTON_WIDTH, 30)

age_label_rect = pygame.Rect(PADDING, name_input_rect.bottom + 10, BUTTON_WIDTH, 30)
age_input_rect = pygame.Rect(age_label_rect.left, age_label_rect.bottom + 5, BUTTON_WIDTH, 30)

# New input fields and labels
patient_number_label_rect = pygame.Rect(PADDING, age_input_rect.bottom + 10, BUTTON_WIDTH, 30)
patient_number_input_rect = pygame.Rect(patient_number_label_rect.left, patient_number_label_rect.bottom + 5, BUTTON_WIDTH, 30)

name_input = ""
age_input = ""
patient_number_input = ""

# Initialize button rectangles
button_gap = 15
button_width_with_gap = (WIDTH // 2 - 3 * PADDING - button_gap) // 2
add_button_rect = pygame.Rect(PADDING, patient_number_input_rect.bottom + 20, button_width_with_gap, 50)
remove_button_rect = pygame.Rect(add_button_rect.right + button_gap, add_button_rect.top, button_width_with_gap, 50)
length_button_rect = pygame.Rect(add_button_rect.left, add_button_rect.bottom + 10, button_width_with_gap, 50)
is_empty_button_rect = pygame.Rect(remove_button_rect.left, remove_button_rect.bottom + 10, button_width_with_gap, 50)
peek_button_rect = pygame.Rect(add_button_rect.left, length_button_rect.bottom + 10, button_width_with_gap, 50)

# Display section dimensions
display_width = WIDTH // 2 - 50  # Adjusted width with a 25px margin on both sides
display_height = 600
display_margin_top = 25
display_margin_bottom = 25

# Variable to keep track of added patients
added_patients = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = event.pos
                # Add patient button
                if is_button_clicked((x, y), add_button_rect) and added_patients < MAX_PATIENTS:
                    # Get patient information from input fields
                    patient_name = name_input
                    patient_age = int(age_input) if age_input.isdigit() else 0

                    # Ensure all fields are filled
                    if not all([patient_name, patient_age]):
                        show_error("Please enter patient information.")
                        continue

                    # Check if max capacity is reached
                    if added_patients >= MAX_PATIENTS and not max_capacity_error_shown:
                        show_max_capacity_error()
                        max_capacity_error_shown = True
                        continue

                    add_patient(patient_name, patient_age)

                    # Clear input fields
                    name_input = ""
                    age_input = ""

                # Remove patient button
                elif is_button_clicked((x, y), remove_button_rect):
                    if priority_queue:
                        heapq.heappop(priority_queue)
                        added_patients -= 1
                        update_patient_numbers()

                # Length button
                elif is_button_clicked((x, y), length_button_rect):
                    show_queue_length()

                # Is Empty button
                elif is_button_clicked((x, y), is_empty_button_rect):
                    check_empty()

                # Peek button
                elif is_button_clicked((x, y), peek_button_rect):
                    peek_at_top()
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos

            # Change cursor to input cursor when hovering over input areas
            if (
                is_input_area_hovered((x, y), name_input_rect)
                or is_input_area_hovered((x, y), age_input_rect)
            ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if is_input_area_hovered(pygame.mouse.get_pos(), name_input_rect):
                    name_input = name_input[:-1]
                elif is_input_area_hovered(pygame.mouse.get_pos(), age_input_rect):
                    age_input = age_input[:-1]
            elif event.key == pygame.K_RETURN:
                # Check if the input field is focused
                if is_input_area_hovered(pygame.mouse.get_pos(), name_input_rect):
                    # Pressing Enter will add a new line in the input field
                    name_input += "\n"
                elif is_input_area_hovered(pygame.mouse.get_pos(), age_input_rect):
                    # Pressing Enter will add the patient with the current input
                    patient_name = name_input
                    patient_age = int(age_input) if age_input.isdigit() else 0

                    # Ensure all fields are filled
                    if not all([patient_name, patient_age]):
                        show_error("Please enter patient information.")
                        continue

                    # Check if max capacity is reached
                    if added_patients >= MAX_PATIENTS:
                        show_max_capacity_error()
                        continue

                    add_patient(patient_name, patient_age)

                    # Clear input fields
                    name_input = ""
                    age_input = ""
                    added_patients += 1

            elif event.unicode.isprintable():
                # Only add printable characters to the input fields
                if (
                    is_input_area_hovered(pygame.mouse.get_pos(), name_input_rect)
                    and event.unicode.isalpha()
                ):
                    name_input += event.unicode
                elif (
                    is_input_area_hovered(pygame.mouse.get_pos(), age_input_rect)
                    and event.unicode.isdigit()
                ):
                    # Limit the input text to stay inside the input area
                    if font.size(age_input + event.unicode)[0] <= age_input_rect.width - 10:
                        age_input += event.unicode

    screen.fill(BACKGROUND)

    # Draw display section with border
    display_rect = pygame.Rect(WIDTH // 2 + 25, display_margin_top, WIDTH // 2 - 50, display_height)
    pygame.draw.rect(screen, WHITE, display_rect)
    pygame.draw.rect(screen, BLACK, display_rect, BORDER_THICKNESS)

    # Draw input labels
    pygame.draw.rect(screen, BACKGROUND, name_label_rect)
    pygame.draw.rect(screen, BACKGROUND, age_label_rect)
    draw_text("Name of Patient:", name_label_rect, color=WHITE)
    draw_text("Age of Patient:", age_label_rect, color=WHITE)

    # Draw input fields with black border
    pygame.draw.rect(screen, BLACK, name_input_rect, BORDER_THICKNESS)
    pygame.draw.rect(screen, WHITE, name_input_rect.inflate(-BORDER_THICKNESS * 2, -BORDER_THICKNESS * 2))
    draw_text(name_input, name_input_rect, color=BLACK)

    pygame.draw.rect(screen, BLACK, age_input_rect, BORDER_THICKNESS)
    pygame.draw.rect(screen, WHITE, age_input_rect.inflate(-BORDER_THICKNESS * 2, -BORDER_THICKNESS * 2))
    draw_text(age_input, age_input_rect, color=BLACK)

    # Draw buttons with centered text
    pygame.draw.rect(screen, (200, 200, 200), add_button_rect)
    pygame.draw.rect(screen, (200, 200, 200), remove_button_rect)
    pygame.draw.rect(screen, (200, 200, 200), length_button_rect)
    pygame.draw.rect(screen, (200, 200, 200), is_empty_button_rect)
    pygame.draw.rect(screen, (200, 200, 200), peek_button_rect)

    draw_text("Add Patient", add_button_rect, color=ORANGE)
    draw_text("Remove Patient", remove_button_rect, color=ORANGE)
    draw_text("Length", length_button_rect, color=ORANGE)
    draw_text("Is Empty", is_empty_button_rect, color=ORANGE)
    draw_text("Peek", peek_button_rect, color=ORANGE)

    # Drawing priority queue
    draw_priority_queue()

    pygame.display.flip()

# Quit Tkinter
root.destroy()
pygame.quit()