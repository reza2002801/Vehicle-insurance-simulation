import State
import random
def starting_state():

    # initialize all state variables
    state = State()

    # Starting FEL
    future_event_list = list()

    r = random.random()
    is_alone = 1 if r < 0.3 else 0

    future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': 0, 'Event Time': 0})  # This is an Event
    return state, future_event_list

def simulation(simulation_time):

    state, future_event_list = starting_state()
    clock = 0
    future_event_list.append({'Event Type': 'End of Simulation', 'Event Time': simulation_time})
    running = True
    id = 0
    while running:
        sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'])

        current_event = sorted_fel[0]  # Find imminent event
        Event_Type = current_event['Event Type']
        clock = current_event['Event Time']  # Advance time
        if Event_Type == 'A':
            pass
        elif Event_Type == 'DP':
            pass
        elif Event_Type == 'DF':
            pass
        elif Event_Type == 'DC':
            pass
        elif Event_Type == 'DE':
            pass
        elif Event_Type == 'DSC':
            pass
        elif Event_Type == 'PA':
            pass
        elif Event_Type == 'OIN':
            pass
        elif Event_Type == 'ISEND':
            pass
        future_event_list.remove(current_event)
