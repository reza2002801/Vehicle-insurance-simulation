import pandas as pd


import random
import math

from States import States


def starting_state():
    """ this is a function to evaluate the initial state of FEL in simulation"""
    # initialize all state variables
    state = States()

    # Starting FEL
    future_event_list = list()

    r = random.random()
    is_alone = 1 if r < 0.3 else 0

    future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': 0, 'Event Time': 0})  # This is an Event

    return state, future_event_list

def simulation():
    """ This is the main function of simulation that handles the modifications that each event notice
    applies on the state valriables
    """
    dataset = pd.read_csv('datasets/Arrival Rate.csv')
    state, future_event_list = starting_state()
    r = random.random()
    weather_condition = 'rainy' if r < 0.31 else 'sunny'
    clock = 0

    running = True
    id = 1

    while running:

        sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'])
        if convert_to_hour(clock) > 18:
            pass
        if id >30:
            break
        current_event = sorted_fel[0]  # Find imminent event


        Event_Type = current_event['Event Type']
        clock = current_event['Event Time']  # Advance time
        if Event_Type == 'A':

            if clock < 600:
                if current_event['alone'] == 0:
                    if state.Length_Service_Photographer == 2:
                        if state.Length_Queue_Photography == 20:
                            state.Length_Queue_OutSide += 1
                            state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                'alone': 0 })
                        else:
                            state.Length_Queue_Photography += 1
                            state.waiting_Queue_Photography.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                'alone': 0, })
                    else:
                        state.Length_Service_Photographer += 1

                        future_event_list.append({'Event Type': 'DP', 'id' : current_event['id'], 'Event Time': clock + sample_exponential(1/6)})
                else:
                    if state.Length_Queue_Photography == 20:
                        state.Length_Queue_OutSide += 1
                        state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                'alone': 1, })
                        future_event_list.append({'Event Type': 'PA', 'id':current_event['id'], 'Event Time': clock + sample_exponential(1/30)})

                    else:
                        state.Length_Waiting_Parking += 1
                        state.waiting_Waiting_Parking.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                'alone': 1, })
                        state.alone_cars_in_parking_id.append(current_event['id'])
                        future_event_list.append({'Event Type': 'PA','id':current_event['id'], 'Event Time': clock + sample_exponential(1/30)})
                r = random.random()
                is_alone = 1 if r < 0.3 else 0
                future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': id, 'Event Time': clock + sample_exponential(1/arrival_rate(weather_condition,clock,dataset))})
                id += 1
                #update cumulative statistics
            else:
                #update the missing customers
                pass
        elif Event_Type == 'DP':
            if state.Length_Queue_Photography == 20:
                state.Length_Queue_Photography -= 1
                customer = state.waiting_Queue_Photography.pop(0)
                if state.Length_Queue_Parking == 0:

                    future_event_list.append({'Event Type': 'OIN', 'id' : state.waiting_Queue_OutSide[0]['id'], 'Event Time': clock })

                else:
                    state.Length_Queue_Photography += 1
                    customer = state.waiting_Queue_Parking.pop(0)
                    state.waiting_Queue_Photography.append({'id': customer['id'], 'alone': 0 })
                    state.Length_Queue_Parking -= 1

                future_event_list.append({'Event Type': 'DP','id': customer['id'] ,'Event Time': clock + sample_exponential(1/6)})


            elif state.Length_Queue_Photography == 0:
                state.Length_Service_Photographer -= 1

            else:
                state.Length_Queue_Photography -= 1
                customer = state.waiting_Queue_Photography.pop(0)
                future_event_list.append({'Event Type': 'DP','id': customer['id']  ,'Event Time': clock + sample_exponential(1/6)})



            if state.Length_Service_Expert1 == 3:
                state.Length_Queue_Filing += 1
                state.waiting_Queue_Filing.append({'id': current_event['id']})

            else:
                state.Length_Service_Expert1 += 1
                future_event_list.append({'Event Type': 'DF','id':current_event['id'], 'Event Time': clock + sample_triangular(5,7,6)})
        elif Event_Type == 'DF':
            if state.Length_Queue_Complete_the_case == 0:
                if state.Length_Queue_Filing == 0:
                    state.Length_Service_Expert1 -= 1

                else:
                    state.Length_Queue_Filing -= 1
                    customer = state.waiting_Queue_Filing.pop(0)
                    future_event_list.append({'Event Type': 'DF','id': customer['id'], 'Event Time': clock + sample_triangular(5,7,6)})
                pass
            else:
                state.Length_Queue_Complete_the_case -= 1
                customer = state.waiting_Queue_Complete_the_case.pop(0)
                future_event_list.append({'Event Type': 'DC','id': customer['id'] ,'Event Time': clock + sample_triangular(6,9,8)})

            if state.Length_Service_Expert2 == 2:
                state.Length_Queue_Expert += 1
                r = random.random()
                complaint = 1 if r < 0.1 else 0
                state.waiting_Queue_Expert.append({'id':current_event['id'],'complaint':complaint})

            else:
                state.Length_Service_Expert2 += 1
                r = random.random()
                complaint = 1 if r < 0.1 else 0
                future_event_list.append(
                    {'Event Type': 'DE', 'complaint': complaint, 'id': current_event['id'], 'Event Time': clock + sample_exponential(1/9)})

        elif Event_Type == 'DC':
            if state.Length_Queue_Complete_the_case == 0:
                if state.Length_Queue_Filing == 0:
                    state.Length_Service_Expert1 -= 1

                else:
                    state.Length_Queue_Filing -= 1
                    customer = state.waiting_Queue_Filing.pop(0)
                    future_event_list.append(
                        {'Event Type': 'DF', 'id': customer['id'], 'Event Time': clock + sample_triangular(5, 7, 6)})
                pass
            else:
                state.Length_Queue_Complete_the_case -= 1
                customer = state.waiting_Queue_Complete_the_case.pop(0)
                future_event_list.append(
                    {'Event Type': 'DC', 'id': customer['id'], 'Event Time': clock + sample_triangular(6, 9, 8)})

            if clock < 600:
                pass
            else:
                if state.Length_Service_Expert1 == 0:
                    future_event_list.append({'Event Type': 'ISEND', 'Event Time': clock})
                    pass
                else:
                    pass
            pass
        elif Event_Type == 'DE':

            if state.Length_Queue_Expert == 0:
                state.Length_Service_Expert2 -= 1

            else:
                state.Length_Queue_Expert -= 1
                customer = state.waiting_Queue_Expert.pop(0)
                future_event_list.append({'Event Type': 'DE','id': customer['id'], 'complaint': customer['complaint'], 'Event Time': clock + sample_exponential(1/9)})

            if current_event['complaint'] == 0:
                if state.Length_Service_Expert1 == 3:
                    state.Length_Queue_Complete_the_case += 1
                    state.waiting_Queue_Complete_the_case.append({'id':current_event['id']})


                else:
                    state.Length_Service_Expert1 += 1
                    future_event_list.append({'Event Type': 'DC','id':current_event['id'], 'Event Time': clock + sample_triangular(6,9,8)})



            else:
                if state.Length_Service_Expert3 == 0:
                    state.Length_Service_Expert3 += 1
                    future_event_list.append({'Event Type': 'DSC','id': current_event['id'], 'Event Time': clock + sample_exponential(1/15)})


                else:
                    state.Length_Queue_Submitting_Complaint += 1
                    state.waiting_Queue_Submitting_Complaint.append({'id':current_event['id']})



            pass
        elif Event_Type == 'DSC':
            if state.Length_Queue_Submitting_Complaint == 0:
                state.Length_Service_Expert3 -= 1
                pass
            else:
                state.Length_Queue_Submitting_Complaint -= 1
                customer = state.waiting_Queue_Submitting_Complaint.pop(0)
                future_event_list.append({'Event Type': 'DSC', 'id': customer['id'],'Event Time': clock + sample_exponential(1/15)})
                pass

            if state.Length_Service_Expert2 == 2:
                state.Length_Queue_Expert += 1
                state.waiting_Queue_Expert.append({'id':current_event['id'],'complaint': 0})
                pass
            else:
                state.Length_Service_Expert2 += 1
                future_event_list.append({'Event Type': 'DE','complaint': 0,'id': current_event['id'], 'Event Time': clock + sample_exponential(1/9)})
                pass

        elif Event_Type == 'PA':

            if current_event['first car id'] not in state.alone_cars_in_parking_id:
                for car in state.waiting_Queue_OutSide:
                    if car['id'] == current_event['first car id']:
                        car['alone'] = 0
                        break


            else:
                temp = False
                state.alone_cars_in_parking_id.remove(current_event['first car id'])
                for car in state.waiting_Waiting_Parking:
                    if car['id'] == current_event['first car id']:
                        temp = car
                        state.waiting_Waiting_Parking.remove(temp)
                        state.Length_Waiting_Parking -= 1
                        temp['alone'] = 0
                        temp = True
                        break

                if state.Length_Service_Photographer == 2:

                    if state.Length_Queue_Photography == 20:
                        state.Length_Queue_Parking += 1
                        state.waiting_Queue_Parking.append(current_event)

                    else:
                        state.Length_Queue_Photography += 1
                        state.waiting_Queue_Photography.append(current_event)
                else:
                    state.Length_Service_Photographer += 1
                    future_event_list.append({'Event Type': 'DP', 'Event Time': clock + sample_exponential(1/6)})
        elif Event_Type == 'OIN':
            if convert_to_hour(clock) < 18:
                if state.Length_Queue_OutSide > 0:
                    car = state.waiting_Queue_OutSide.pop(0)
                    state.Length_Queue_OutSide -= 1

                    if car['alone'] == 0:
                        state.Length_Queue_Photography += 1
                        state.waiting_Queue_Photography.append(car)

                    else:
                        state.Length_Waiting_Parking += 1
                        state.waiting_Waiting_Parking.append(car)


                        state.alone_cars_in_parking_id.append(car['id'])

                        future_event_list.append({'Event Type': 'OIN', 'Event Time': clock })

                else:
                    pass
            else:
                state.Length_Queue_OutSide = 0
                state.waiting_Queue_OutSide.clear()

        elif Event_Type == 'ISEND':
            if state.Length_Waiting_Parking == 0:
                if state.Length_Service_Photographer == 0:
                    if state.Length_Service_Expert2 == 0:
                        if state.Length_Service_Expert3 == 0:
                            running = False
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
            pass
        print(state,'\n\n')
        print(sorted_fel,)
        future_event_list.remove(current_event)

    print('done')
def sample_exponential(lambda_val):
    """this is a function to sample from an exponential distribution with
    lambda: lambda_val using uniform value """
    r = random.random()
    return (-1/lambda_val)*math.log((1-r),math.e)

def sample_triangular(min, max, mod):
    """this is a function to sample from a triangular distribution with
        mod, min and max using uniform distribution """

    r = random.random()
    threshold = (mod - min)/(max - min)
    if r < threshold:
        return math.sqrt(r*(max-min)*(mod-min)) + min
    else:
        return max - math.sqrt((1-r)*(max-min)*(max-mod))

def arrival_rate(weather_condition, time, dataset):
    """ this is a function to find the arrival rate using weather condition and time of the
    day from the arrival rate data set"""

    hour = time/60 + 8
    w = 0 if weather_condition == 'rainy' else 1
    times = [8, 10, 13, 15]
    group = -1
    for t in times:
        if hour >= t:
            group += 1
        else:
            break
    return dataset.iloc[w,group+1]

def convert_to_hour(time):
    return 8 + time/60

simulation()

