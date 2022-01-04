#############################################################
# FILE : wave_editor.py
# WRITER : Sagi Kelner , skelner , Yuval Gonen , yuval
# EXERCISE : intro2cs ex6 2018-2019
# DESCRIPTION : Program for editing wav audio files.
#############################################################

import wave_helper
from copy import deepcopy
import math
import os


# ===  MAGIC NUMBERS === #

MAX_VOLUME = 32767
MIN_VOLUME = -32768
SAMPLE_RATE = 2000


# === GLOBAL MESSAGES === #

ENTRY_MESSAGE = "\nWelcome your Highness\n" \
                "Please select one of the following options - " \
                "Write down the selection number:\n" \
                "1. Edit wav file.\n" \
                "2. Consolidate two wav files.\n" \
                "3. Compose a majestic melody.\n" \
                "4. Exit.\n\n  " \
                "Your choice my King? ->"

EXIT_MESSAGE = "\nLong live the King!"

INPUT_NOT_DIGIT = "\nAlthough you are a King, this choice is not possible.\n" \
                            "Your input is not a number."

INPUT_NUM_NO_EXIST = "\nYour number input does not exist in the " \
                               "selection options my King.."

TRANSITION_MESSAGE = "\nPlease select one of the following options - " \
                "Write down the selection number:\n" \
                "1. Save the new audio you just made as a wav file.\n" \
                "2. Edit the new audio you just made.\n\n  " \
                "Your choice my King? ->"

SAVE_SUCCEEDED_1 = "\nA truly majestic work, well done!\n" \
                   "Your new audio file has been successfully saved as: "

SAVE_SUCCEEDED_2 = "\nLet me kindly take you back to the start menu " \
                   "and bless you again."

SAVE_PROBLEM = "\nThere was a problem with the save process, " \
               "please do not cut my head off!\n" \
               "Maybe think of another name.."

SAVE_QUESTION = "\nWhich name would you like to " \
                "grant to the new file?"

EDIT_BLESSING = "\nYou have reached the 'Execution Room' my lord."

EDIT_MESSAGE = "Please select one of the following options - " \
               "Write down the selection number:\n" \
               "1. Reverse Play.\n" \
               "2. Accelerate the Audio speed (by 2 times).\n" \
               "3. Slow down the Audio speed (by 2 times).\n" \
               "4. Increase Audio volume (volume up by 1.2 times).\n" \
               "5. Decrease Audio volume (volume down by 1.2 times).\n" \
               "6. Dim the Audio.\n\n  " \
               "The King's Command? ->"

EDITING_R = "\nThe 'Reverse' command was successfully executed."
EDITING_A = "\nThe 'Accelerate Audio Speed' command was successfully executed."
EDITING_S = "\nThe 'Slow Audio Speed' command was successfully executed."
EDITING_U = "\nThe 'Volume Up' command was successfully executed."
EDITING_P = "\nThe 'Volume Down' command was successfully executed."
EDITING_D = "\nThe 'Dimming Filter' command was successfully executed."

UNION_M = "\nYour Grace, your wish is my command. The files has been " \
          "successfully merged."


# === THE PROGRAM === #

def main_process():
    """The main process that runs the program. Run by a loop that gets a
     True or False value from the start menu function."""
    repeat = True
    while repeat:
        repeat = start_menu()
    return None


def start_menu():
    """The function prints the Start menu message and waits for input from the
    user. The function transfer to other functions, but each part returns a
    True value, except when pressing the number '4' (exit). In addition, it
    also prints a typo message and waits for additional input."""
    user_choice = input(ENTRY_MESSAGE)
    if user_choice.isdigit():

        if int(user_choice) == 1:  # EDIT
            repeat = True
            while repeat is True:
                wav_file_name = input("\nwave file name:")
                repeat = load_file_and_validate(wav_file_name)
            return edit_audio_menu(repeat[0], repeat[1])

        elif int(user_choice) == 2:  # UNION
            repeat = True
            while repeat is True:
                wav_file_name = input("\nThe names of the wave files (Please "
                                      "place a space between them):")
                repeat = load_files_and_validate(wav_file_name)
            audio_data = unify_audio(repeat)
            return transition_menu(audio_data[0], audio_data[1])

        elif int(user_choice) == 3:  # COMPOSING
            repeat = True
            while repeat is True:
                composing_file_name = input("\nComposing file name:")
                repeat = file_to_compose_list(composing_file_name)

            audio_data = (SAMPLE_RATE, composed_audio_list(repeat))
            return transition_menu(audio_data[0], audio_data[1])

        elif int(user_choice) == 4:  # EXIT
            print(EXIT_MESSAGE)
            return False

        else:
            print(INPUT_NUM_NO_EXIST + "\nTry again.")
            return True
    else:
        print(INPUT_NOT_DIGIT + "\nTry again.")
        return True


def edit_audio_menu(frame_rate, audio_list):
    """The function prints the Edit menu message and waits for input from the
    user. The function transfer to other functions, according to the input. The
    function gets audio data and returns the new edit data in transition
    function. In addition, it also prints a typo message and waits for
    additional input."""
    invalid_input = True
    print(EDIT_BLESSING)
    while invalid_input:
        user_choice = input(EDIT_MESSAGE)
        if user_choice.isdigit():

            if int(user_choice) == 1:  # REVERSE
                new_audio_list = reverse_audio(audio_list)
                print(EDITING_R)
                return transition_menu(frame_rate, new_audio_list)
            elif int(user_choice) == 2:  # ACCELERATE
                new_audio_list = accelerate_audio_speed(audio_list)
                print(EDITING_A)
                return transition_menu(frame_rate, new_audio_list)
            elif int(user_choice) == 3:  # SLOW DOWN
                new_audio_list = slow_audio_speed(audio_list)
                print(EDITING_S)
                return transition_menu(frame_rate, new_audio_list)
            elif int(user_choice) == 4:  # VOLUME UP
                new_audio_list = volume_up(audio_list)
                print(EDITING_U)
                return transition_menu(frame_rate, new_audio_list)
            elif int(user_choice) == 5:  # VOLUME DOWN
                new_audio_list = volume_down(audio_list)
                print(EDITING_D)
                return transition_menu(frame_rate, new_audio_list)
            elif int(user_choice) == 6:  # DIMMING
                new_audio_list = dimming_filter(audio_list)
                print(EDITING_D)
                return transition_menu(frame_rate, new_audio_list)

            else:
                print(INPUT_NUM_NO_EXIST)
                continue
        else:
            print(INPUT_NOT_DIGIT)
            continue


def transition_menu(frame_rate, audio_list):
    """The function prints the Transition menu message and waits for input from
    the user. The function transfer to other functions, according to the input.
    The function gets audio data and returns True If the save process has
    passed successfully and if the user want to edit, it return the Edit
    function with the audio data. In addition, it also prints a typo message
    and waits for additional input."""
    invalid_input = True
    while invalid_input:
        user_choice = input(TRANSITION_MESSAGE)
        if user_choice.isdigit():

            if int(user_choice) == 1:  # SAVE
                repeat = True
                new_file_name = ""
                while repeat:
                    new_file_name = input(SAVE_QUESTION)

                    repeat = wave_helper.save_wave(frame_rate, audio_list,
                                                   new_file_name)
                    if repeat == 0:
                        break
                    print(SAVE_PROBLEM)
                print(SAVE_SUCCEEDED_1 + new_file_name + SAVE_SUCCEEDED_2)
                return True

            elif int(user_choice) == 2:  # EDIT
                return edit_audio_menu(frame_rate, audio_list)

            else:
                print(INPUT_NUM_NO_EXIST)
                continue
        else:
            print(INPUT_NOT_DIGIT)
            continue


# === AUXILIARY FUNCTIONS FOR *EDIT* === #

def load_file_and_validate(file_name):
    """Gets a name of the wav file and returns the audio data. Prints messages
    if there is typo or the file is not found and return True."""
    audio_data = wave_helper.load_wave(file_name)
    if audio_data != -1:
        return audio_data

    else:  # File not found / invalid filename
        if ".wav" not in file_name:
            print("""\nInvalid filename - No ".wav" extension found.""")
        else:
            print("\nFile does not exist.\nPlease try again.")
        return True


def reverse_audio(audio_list):
    """Gets a list and returns a list in which the items are arranged in
    reverse order."""
    audio_list.reverse()
    return audio_list


def accelerate_audio_speed(audio_list):
    """Return list of items whose index is even from a given list."""
    new_audio_list = []
    for i in range(0, len(audio_list), 2):
        temp_item = audio_list[i]
        new_audio_list.append(temp_item)
    return new_audio_list


def slow_audio_speed(audio_list):
    """Gets a list and returns a list with average objects between each
    original object."""
    new_audio_list = [audio_list[0]]
    for i in range(1, len(audio_list)):
        average_item = [int((audio_list[i-1][0] + audio_list[i][0])/2),
                        int((audio_list[i-1][1] + audio_list[i][1])/2)]
        new_audio_list.append(average_item)
        new_audio_list.append(audio_list[i])
    return new_audio_list


def volume_change(audio_list, volume):
    """Receives a list and volume power and returns a list in which the values
    are multiplied by power and are also valid values."""
    new_audio_list = []
    for i in range(len(audio_list)):
        changed_item = [int(audio_list[i][0] * volume),
                        int(audio_list[i][1] * volume)]

        for j in range(2):  # Check if we have passed the valid values
            if changed_item[j] < MIN_VOLUME:
                changed_item[j] = MIN_VOLUME
            if changed_item[j] > MAX_VOLUME:
                changed_item[j] = MAX_VOLUME
        new_audio_list.append(changed_item)
    return new_audio_list


def volume_up(audio_list):
    """Receives a list and returns a list in which the values are
    multiplied by 1.2."""
    up_value = 1.2
    return volume_change(audio_list, up_value)


def volume_down(audio_list):
    """Receives a list and returns a list in which the values are
    divided by 1.2."""
    down_value = (1 / 1.2)
    return volume_change(audio_list, down_value)


def dimming_filter(audio_list):
    """Gets a list and returns a list of averages between each tree
    close items, at the edges between two close items."""
    new_audio_list = []
    tem_audio_list = slow_audio_speed(audio_list)
    new_audio_list.append(tem_audio_list[1])
    for i in range(1, len(audio_list)-1):
        average_item = \
            [int((audio_list[i - 1][0] + audio_list[i][0] +
                  audio_list[i + 1][0]) / 3),
             int((audio_list[i - 1][1] + audio_list[i][1] +
                  audio_list[i + 1][1]) / 3)]
        new_audio_list.append(average_item)
    new_audio_list.append(tem_audio_list[-2])
    return new_audio_list


# === AUXILIARY FUNCTIONS FOR *COMPOSING* === #

def file_to_compose_list(file_name):
    """Gets a file name and if the file exist, it returns a list of the
    letters and numbers written in the file. If it does not exist - Printing a
    message according to the error and return True."""

    if os.path.isfile(file_name):
        compose_list = []
        compose_file = open(file_name)
        for line in compose_file.readlines():
            compose_list += line.strip('\n').split(' ')
        while '' in compose_list:
            compose_list.remove('')
        compose_file.close()
        return compose_list

    else:  # File not found / invalid filename
        if ".txt" not in file_name:
            print("""\nInvalid filename - No ".txt" extension found.""")
        else:
            print("\nFile does not exist.\nPlease try again.")
        return True


def note_to_frequency(note):
    """Receives a letter (note) and returns its frequency value."""
    conversion_dictionary = {"Q": 0, "A": 440, "B": 494, "C": 523, "D": 587,
                             "E": 659, "F": 698, "G": 784}
    return conversion_dictionary[note]


def number_to_samples_amount(number):
    """Receives a number and returns the number of samples per second."""
    samples_amount = int(number/16 * SAMPLE_RATE)
    return samples_amount


def formula(frequency, index):
    """Gets frequency and index and returns the value of the written
    formula."""
    if frequency == 0:
        result = 0
    else:
        samples_per_cycle = SAMPLE_RATE/frequency
        result = \
            int(MAX_VOLUME * math.sin(math.pi * 2 * index/samples_per_cycle))
    return result


def audio_list_for_note_and_number(note, number):
    """Receives one letter (note) and one number and returns an audio list
    of them."""
    audio_list = []
    for i in range(number_to_samples_amount(number)):
        temp_list = [formula(note_to_frequency(note), i)]
        temp_list.append(temp_list[0])
        audio_list.append(temp_list)
    return audio_list


def composed_audio_list(compose_list):
    """Receives a list consisting of letters (notes) and numbers and returns a
    composed audio list."""
    audio_list = []
    for i in range(0, len(compose_list), 2):
        temp_list = audio_list_for_note_and_number(compose_list[i],
                                                   int(compose_list[i + 1]))
        audio_list += temp_list
    return audio_list


# === AUXILIARY FUNCTIONS FOR *UNION* === #

def load_files_and_validate(files_name):
    """Gets a files name(str) and if the files exist, it returns a tuple
    containing the two frame rate and the two audio list. If it does not exist
    - from any reason, it prints accordingly message and return true."""
    if " " not in files_name:
        print("\nThere is no space between the names of the files my Lord")
        return True
    files_name_list = files_name.split(" ")
    if len(files_name_list) > 2 or len(files_name_list) < 2:
        print("\nYou must enter exactly 2 file names and not more or less. "
              "In addition, make sure you only have one space in your input")
        return True
    file1_data = wave_helper.load_wave(files_name_list[0])
    file2_data = wave_helper.load_wave(files_name_list[1])

    if file1_data != -1 and file2_data != -1:
        return file1_data[0], file2_data[0], file1_data[1], file2_data[1]

    else:  # File not found / invalid filename
        if ".wav" not in files_name_list[0] or \
                ".wav" not in files_name_list[1]:
            print("""\nInvalid filename - No ".wav" extension found.""")
        else:
            print("\nFile does not exist.\nPlease try again.")
        return True


def unify_audio(two_audio_data):
    """ This function compares the frame rates of both audio lists.
    if it's not the same, different_frame_rate is activated. Otherwise,
    unify_audio_lst is activated. In addition the final frame rate is set to
    be the smaller one. """
    data = two_audio_data
    if data:
        if data[0] != data[1]:
            if data[0] < data[1]:         # frame_rate1 < frame_rate2
                frame_rate = data[0]
            else:
                frame_rate = data[1]
            print(UNION_M)
            return frame_rate, different_frame_rate(data[0], data[1],
                                                    data[2], data[3])
        else:
            print(UNION_M)
            return data[0], unify_audio_lst(data[2], data[3])


def average_lst(audio_lst1, audio_lst2):
    """This function creates a list of lists in the length of the longer
    list out of the audio lists. Each inner list contains two zeros for now."""
    avg_lst = []
    if len(audio_lst1) >= len(audio_lst2):
        max_audio = audio_lst1
    else:
        max_audio = audio_lst2
    for i in range(len(max_audio)):
        avg_lst.append([0, 0])
    return avg_lst


def same_len_avg(audio_lst1, audio_lst2):
    """When both audio lists are in the same size, this function changes
    the values of avg_lst to the average of both audio lists accordingly."""
    avg_lst = average_lst(audio_lst1, audio_lst2)   # list of lists of zeros
    for i in range(len(audio_lst2)):                # audio_lst2 on purpose
        avg_lst[i][0] = int((audio_lst1[i][0] + audio_lst2[i][0]) / 2)
        avg_lst[i][1] = int((audio_lst1[i][1] + audio_lst2[i][1]) / 2)
    updated_avg_lst = check_avg_in_range(avg_lst)
    return updated_avg_lst


def check_avg_in_range(avg_lst):
    """This function makes sure that the average that we calculated is in
    range."""
    for j in range(len(avg_lst)):
        for k in range(2):
            if avg_lst[j][k] > MAX_VOLUME:
                avg_lst[j][k] = MAX_VOLUME
            if avg_lst[j][k] < MIN_VOLUME:
                avg_lst[j][k] = MIN_VOLUME
    return avg_lst


def unify_audio_lst(audio_lst1, audio_lst2):
    """This function unifies two audio lists based on their length."""
    if len(audio_lst1) == len(audio_lst2):
        return same_len_avg(audio_lst1, audio_lst2)
    elif len(audio_lst1) > len(audio_lst2):
        return diff_len_avg(audio_lst1, audio_lst2)
    else:
        return diff_len_avg(audio_lst2, audio_lst1)


def diff_len_avg(audio_lst1, audio_lst2):
                                # assume len(audio_lst1) > len(audio_lst2)
    """When the length of the audio lists is different, this function changes
    the values of temp_lst. While the length is the same, it uses the
    'same_len_avg' function, and then adds the items of the longer list."""
    zeros_lst = average_lst(audio_lst1, audio_lst2)
    min_len = len(audio_lst2)
    add_lst = zeros_lst[min_len:]      # we don't need all the list
    temp_lst = deepcopy(audio_lst1[:min_len])
    avg_lst = same_len_avg(temp_lst, audio_lst2) + add_lst
    for i in range(min_len, len(audio_lst1)):
        avg_lst[i] = audio_lst1[i]                  # changing the zeros to the
    updated_avg_lst = check_avg_in_range(avg_lst)   # items of the longer list
    return updated_avg_lst

# from now on frame_rate1 != frame_rate2:


def find_longer_lst(audio_lst1, audio_lst2):
    """This function finds the longer list out of the audio lists."""
    if len(audio_lst1) >= len(audio_lst2):
        max_audio = audio_lst1
    else:
        max_audio = audio_lst2
    return deepcopy(max_audio)


def divide_lst_helper(frame_rate1, frame_rate2, audio_lst1, audio_lst2):
    """This function divides the longer audio list to smaller lists in the
    size of (frame rate / gcd). All these smaller lists are in one long list.
    This function excludes the modulo."""
    gcd = math.gcd(frame_rate1, frame_rate2)
    max_num = int(max(frame_rate1, frame_rate2) / gcd)
    new_lst = []
    max_lst = find_longer_lst(audio_lst1, audio_lst2)
    for i in range(int(len(max_lst)/max_num)):
        new_lst.append([])    # create empty lists in the needed amount
    start = 0
    stop = max_num
    while stop <= len(max_lst):
        for i in range(len(new_lst)):
            for j in range(start, stop):
                new_lst[i].append(list((max_lst[j])))
            start += max_num
            stop += max_num
    return gcd, max_num, max_lst, new_lst


def divide_lst(frame_rate1, frame_rate2, audio_lst1, audio_lst2):
    """This function takes the list from the former function and adds a
    list of the modulo."""
    gcd, max_num, max_lst, new_lst = \
        divide_lst_helper(frame_rate1, frame_rate2, audio_lst1, audio_lst2)
    modulo = len(max_lst) % max_num
    if modulo != 0:
        new_lst.append([])

    for j in range(modulo, 0, -1):
        new_lst[-1].append(max_lst[-j])

    return gcd, modulo, new_lst


def reduced_list(frame_rate1, frame_rate2, audio_lst1, audio_lst2):
    """This function takes the needed amount of items from each inner list."""
    gcd, modulo, lst = divide_lst(frame_rate1, frame_rate2,
                                  audio_lst1, audio_lst2)
    min_num = int(min(frame_rate1, frame_rate2) / gcd)
    new_lst = []
    if modulo == 0:
        for inner_lists in lst:
            for j in range(min_num):
                    new_lst.append(inner_lists[j])
    else:
        new_lst = modulo_not_zero(frame_rate1, frame_rate2,
                                  audio_lst1, audio_lst2)
    return new_lst


def modulo_not_zero(frame_rate1, frame_rate2, audio_lst1, audio_lst2):
    """This function helps the former one when the modulo is not zero."""
    gcd, modulo, lst = divide_lst(frame_rate1, frame_rate2,
                                  audio_lst1, audio_lst2)
    min_num = int(min(frame_rate1, frame_rate2) / gcd)
    new_lst = []
    for inner_lists in lst[:-1]:
        for j in range(min_num):
            new_lst.append(inner_lists[j])
    if modulo == 1:
        new_lst.extend(lst[-1])
    elif len(lst[-1]) < min_num:
        new_lst.append(lst[-1])
    else:
        for j in range(min_num):
            new_lst.append(lst[-1][j])
    return new_lst


def different_frame_rate(frame_rate1, frame_rate2, audio_lst1, audio_lst2):
    """This function takes the shorter list that was created in the former
    functions and unifies it with another audio list."""
    new_lst = reduced_list(frame_rate1, frame_rate2, audio_lst1, audio_lst2)
    if len(audio_lst1) >= len(audio_lst2):
        return unify_audio_lst(new_lst, audio_lst2)
    else:
        return unify_audio_lst(audio_lst1, new_lst)


if __name__ == '__main__':
    main_process()
