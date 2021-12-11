-module(shipping).
-compile(export_all).
-include_lib("./shipping.hrl").

% Rafael Sanchez & Tudor Rus
% I pledge my honor that I have abided by the Stevens Honor System.

get_ship(Shipping_State, Ship_ID) ->
    B=lists:keyfind(Ship_ID, #ship.id, Shipping_State#shipping_state.ships),
    if 
        B=/=false -> B;
        true -> error 
    end. 

get_container(Shipping_State, Container_ID) ->
    B=lists:keyfind(Container_ID, #container.id, Shipping_State#shipping_state.containers),
    if 
        B=/=false -> B;
        true -> error 
    end. 

get_port(Shipping_State, Port_ID) ->
    B=lists:keyfind(Port_ID, #port.id, Shipping_State#shipping_state.ports),
    if 
        B=/=false -> B;
        true -> error 
    end.

get_occupied_docks_helper(Port_ID, All_Locations, Found_Docks) ->
    Tuple = lists:keyfind(Port_ID, 1, All_Locations),
    case Tuple of
        false -> Found_Docks;
        {_E1, E2, _E3} -> get_occupied_docks_helper(Port_ID, lists:keydelete(Port_ID, 1 , All_Locations), Found_Docks ++ [E2])
    end.
    

get_occupied_docks(Shipping_State, Port_ID) ->
    case Shipping_State#shipping_state.ship_locations of
        [] -> [];
        [H | T] -> get_occupied_docks_helper(Port_ID, [H | T], [])
    end.
    
get_ship_location(Shipping_State, Ship_ID) ->
    B=lists:keyfind(Ship_ID, 3, Shipping_State#shipping_state.ship_locations),
    case B of
        {E1, E2, _E3} -> {E1, E2};
        false -> error
    end.

get_container_weight_helper(Shipping_State, Container_IDs, Acc) ->
    case Container_IDs of
        [] -> Acc;
        [H | T] -> B=get_container(Shipping_State, H), if 
                                                            B==error -> error;
                                                            true -> get_container_weight_helper(Shipping_State, T, Acc + B#container.weight)
                                                        end
    end.

get_container_weight(Shipping_State, Container_IDs) ->
    get_container_weight_helper(Shipping_State, Container_IDs, 0).

get_ship_weight(Shipping_State, Ship_ID) ->
    Map = Shipping_State#shipping_state.ship_inventory,
    Key = Ship_ID,
    case maps:find(Key, Map) of
        {ok,[]} -> 0;
        {ok,[H | T]} -> get_container_weight(Shipping_State, [H | T]);
        error -> error
    end.

load_ship_helper(The_Ship_Inventory, All_Portids, Shipping_State, Ship_ID, Container_IDs, Portid) ->
    ShipData = get_ship(Shipping_State, Ship_ID),
    Capacity = ShipData#ship.container_cap,
    Can_load_capacity = ((length(The_Ship_Inventory) + length(Container_IDs)) =< Capacity),
    Can_load_samePort = is_sublist(All_Portids, Container_IDs),
    if 
        Can_load_capacity==true andalso Can_load_samePort==true -> {ok, #shipping_state{
                                                                        ships = Shipping_State#shipping_state.ships,
                                                                        containers = Shipping_State#shipping_state.containers,
                                                                        ports = Shipping_State#shipping_state.ports,
                                                                        ship_locations = Shipping_State#shipping_state.ship_locations,
                                                                        ship_inventory = maps:put(Ship_ID, The_Ship_Inventory ++ Container_IDs, Shipping_State#shipping_state.ship_inventory),
                                                                        port_inventory = maps:put(Portid, lists:subtract(All_Portids, Container_IDs), Shipping_State#shipping_state.port_inventory)}}; 
        Can_load_capacity==false orelse Can_load_samePort==false -> error
    end.

load_ship(Shipping_State, Ship_ID, Container_IDs) ->
    Tuple = get_ship_location(Shipping_State, Ship_ID),
    case Tuple of
       {Portid, _Dockstr} -> case Container_IDs of
                                [] -> {ok, Shipping_State};
                                [_H | _T] -> MapShipInv = Shipping_State#shipping_state.ship_inventory,
                                             KeyShip = Ship_ID,
                                             case maps:find(KeyShip, MapShipInv) of
                                                {ok, The_Ship_Inventory} -> MapPortInv = Shipping_State#shipping_state.port_inventory, 
                                                                            KeyPort = Portid, 
                                                                            case maps:find(KeyPort, MapPortInv) of
                                                                                {ok, All_Portids} -> load_ship_helper(The_Ship_Inventory, All_Portids, Shipping_State, Ship_ID, Container_IDs, Portid);
                                                                                error -> error
                                                                            end;
                                                error -> error
                                            end
                             end;
       error -> error
    end.

unload_ship_all_helper(The_Ship_Inventory, All_Portids, Shipping_State, Ship_ID, Portid) ->
    PortData = get_port(Shipping_State, Portid),
    Capacity = PortData#port.container_cap,
    Can_load_capacity = ((length(The_Ship_Inventory) + length(All_Portids)) =< Capacity),
    if
        Can_load_capacity==true -> {ok, #shipping_state{
                                            ships = Shipping_State#shipping_state.ships,
                                            containers = Shipping_State#shipping_state.containers,
                                            ports = Shipping_State#shipping_state.ports,
                                            ship_locations = Shipping_State#shipping_state.ship_locations,
                                            ship_inventory = maps:put(Ship_ID, [], Shipping_State#shipping_state.ship_inventory),
                                            port_inventory = maps:put(Portid, All_Portids ++ The_Ship_Inventory, Shipping_State#shipping_state.port_inventory)}};
        Can_load_capacity==false -> error
    end.


unload_ship_all(Shipping_State, Ship_ID) ->
    Tuple = get_ship_location(Shipping_State, Ship_ID),
    case Tuple of
        {Portid, _Dockstr} -> MapShipInv = Shipping_State#shipping_state.ship_inventory,
                              KeyShip = Ship_ID,
                              case maps:find(KeyShip, MapShipInv) of
                                  {ok, The_Ship_Inventory} -> MapPortInv = Shipping_State#shipping_state.port_inventory,
                                                              KeyPort = Portid,
                                                              case maps:find(KeyPort, MapPortInv) of
                                                                  {ok, All_Portids} -> unload_ship_all_helper(The_Ship_Inventory, All_Portids, Shipping_State, Ship_ID, Portid);
                                                                  error -> error
                                                              end;
                                  error -> error
                              end;
        error -> error
    end.

unload_ship_helper(The_Ship_Inventory, All_Portids, Shipping_State, Ship_ID, Container_IDs, Portid) ->
    PortData = get_port(Shipping_State, Portid),
    Capacity = PortData#port.container_cap,
    Can_load_capacity = ((length(All_Portids) + length(Container_IDs)) =< Capacity),
    Can_load_samePort = is_sublist(The_Ship_Inventory, Container_IDs),
    if 
        Can_load_capacity==true andalso Can_load_samePort==true -> {ok, #shipping_state{
                                                                        ships = Shipping_State#shipping_state.ships,
                                                                        containers = Shipping_State#shipping_state.containers,
                                                                        ports = Shipping_State#shipping_state.ports,
                                                                        ship_locations = Shipping_State#shipping_state.ship_locations,
                                                                        ship_inventory = maps:put(Ship_ID, lists:subtract(The_Ship_Inventory, Container_IDs), Shipping_State#shipping_state.ship_inventory),
                                                                        port_inventory = maps:put(Portid, All_Portids ++ Container_IDs, Shipping_State#shipping_state.port_inventory)}}; 
        Can_load_samePort==false -> io:format("The given containers are not all on the same ship...~n"), error;
        Can_load_capacity==false -> error 
    end.

unload_ship(Shipping_State, Ship_ID, Container_IDs) ->
    Tuple = get_ship_location(Shipping_State, Ship_ID),
    case Tuple of
       {Portid, _Dockstr} -> case Container_IDs of
                                [] -> {ok, Shipping_State};
                                [_H | _T] -> MapShipInv = Shipping_State#shipping_state.ship_inventory,
                                             KeyShip = Ship_ID,
                                             case maps:find(KeyShip, MapShipInv) of
                                                {ok, The_Ship_Inventory} -> MapPortInv = Shipping_State#shipping_state.port_inventory, 
                                                                            KeyPort = Portid, 
                                                                            case maps:find(KeyPort, MapPortInv) of
                                                                                {ok, All_Portids} -> unload_ship_helper(The_Ship_Inventory, All_Portids, Shipping_State, Ship_ID, Container_IDs, Portid);
                                                                                error -> error
                                                                            end;
                                                error -> error
                                            end
                             end;
       error -> error
    end.

set_sail_helper2(Occupied_Ports_Docks_Tuple_List, Dock) ->
    Tuple = lists:keyfind(Dock, 2, Occupied_Ports_Docks_Tuple_List),
    case Tuple of
        false -> proceed;
        {_E1, _E2} -> error
    end.

set_sail_helper(Port_ID, All_Locations, Found_Tuples) ->
    Tuple = lists:keyfind(Port_ID, 1, All_Locations),
    case Tuple of
        false -> Found_Tuples;
        {E1, E2, _E3} -> set_sail_helper(Port_ID, lists:keydelete(Port_ID, 1, All_Locations), Found_Tuples ++ [{E1, E2}])
    end.

set_sail(Shipping_State, Ship_ID, {Port_ID, Dock}) -> 
    case Shipping_State#shipping_state.ship_locations of
        [] -> {ok, #shipping_state{
                                        ships = Shipping_State#shipping_state.ships,
                                        containers = Shipping_State#shipping_state.containers,
                                        ports = Shipping_State#shipping_state.ports,
                                        ship_locations = 
                                        ship_inventory = lists:keyreplace(Ship_ID, 3, Shipping_State#shipping_state.ship_locations, {Port_ID, Dock, Ship_ID}),
                                        port_inventory = Shipping_State#shipping_state.port_inventory}}; % Set Sail
        [H | T] -> case set_sail_helper2(set_sail_helper(Port_ID, [H | T], []), Dock) of
                        proceed -> {ok, #shipping_state{
                                        ships = Shipping_State#shipping_state.ships,
                                        containers = Shipping_State#shipping_state.containers,
                                        ports = Shipping_State#shipping_state.ports,
                                        ship_locations = lists:keyreplace(Ship_ID, 3, Shipping_State#shipping_state.ship_locations, {Port_ID, Dock, Ship_ID}),
                                        ship_inventory = Shipping_State#shipping_state.ship_inventory,
                                        port_inventory = Shipping_State#shipping_state.port_inventory}};
                        error -> error
                    end
    end.


%% Determines whether all of the elements of Sub_List are also elements of Target_List
%% @returns true is all elements of Sub_List are members of Target_List; false otherwise
is_sublist(Target_List, Sub_List) ->
    lists:all(fun (Elem) -> lists:member(Elem, Target_List) end, Sub_List).




%% Prints out the current shipping state in a more friendly format
print_state(Shipping_State) ->
    io:format("--Ships--~n"),
    _ = print_ships(Shipping_State#shipping_state.ships, Shipping_State#shipping_state.ship_locations, Shipping_State#shipping_state.ship_inventory, Shipping_State#shipping_state.ports),
    io:format("--Ports--~n"),
    _ = print_ports(Shipping_State#shipping_state.ports, Shipping_State#shipping_state.port_inventory).


%% helper function for print_ships
get_port_helper([], _Port_ID) -> error;
get_port_helper([ Port = #port{id = Port_ID} | _ ], Port_ID) -> Port;
get_port_helper( [_ | Other_Ports ], Port_ID) -> get_port_helper(Other_Ports, Port_ID).


print_ships(Ships, Locations, Inventory, Ports) ->
    case Ships of
        [] ->
            ok;
        [Ship | Other_Ships] ->
            {Port_ID, Dock_ID, _} = lists:keyfind(Ship#ship.id, 3, Locations),
            Port = get_port_helper(Ports, Port_ID),
            {ok, Ship_Inventory} = maps:find(Ship#ship.id, Inventory),
            io:format("Name: ~s(#~w)    Location: Port ~s, Dock ~s    Inventory: ~w~n", [Ship#ship.name, Ship#ship.id, Port#port.name, Dock_ID, Ship_Inventory]),
            print_ships(Other_Ships, Locations, Inventory, Ports)
    end.

print_containers(Containers) ->
    io:format("~w~n", [Containers]).

print_ports(Ports, Inventory) ->
    case Ports of
        [] ->
            ok;
        [Port | Other_Ports] ->
            {ok, Port_Inventory} = maps:find(Port#port.id, Inventory),
            io:format("Name: ~s(#~w)    Docks: ~w    Inventory: ~w~n", [Port#port.name, Port#port.id, Port#port.docks, Port_Inventory]),
            print_ports(Other_Ports, Inventory)
    end.
%% This functions sets up an initial state for this shipping simulation. You can add, remove, or modidfy any of this content. This is provided to you to save some time.
%% @returns {ok, shipping_state} where shipping_state is a shipping_state record with all the initial content.
shipco() ->
    Ships = [#ship{id=1,name="Santa Maria",container_cap=20},
              #ship{id=2,name="Nina",container_cap=20},
              #ship{id=3,name="Pinta",container_cap=20},
              #ship{id=4,name="SS Minnow",container_cap=20},
              #ship{id=5,name="Sir Leaks-A-Lot",container_cap=20}
             ],
    Containers = [
                  #container{id=1,weight=200},
                  #container{id=2,weight=215},
                  #container{id=3,weight=131},
                  #container{id=4,weight=62},
                  #container{id=5,weight=112},
                  #container{id=6,weight=217},
                  #container{id=7,weight=61},
                  #container{id=8,weight=99},
                  #container{id=9,weight=82},
                  #container{id=10,weight=185},
                  #container{id=11,weight=282},
                  #container{id=12,weight=312},
                  #container{id=13,weight=283},
                  #container{id=14,weight=331},
                  #container{id=15,weight=136},
                  #container{id=16,weight=200},
                  #container{id=17,weight=215},
                  #container{id=18,weight=131},
                  #container{id=19,weight=62},
                  #container{id=20,weight=112},
                  #container{id=21,weight=217},
                  #container{id=22,weight=61},
                  #container{id=23,weight=99},
                  #container{id=24,weight=82},
                  #container{id=25,weight=185},
                  #container{id=26,weight=282},
                  #container{id=27,weight=312},
                  #container{id=28,weight=283},
                  #container{id=29,weight=331},
                  #container{id=30,weight=136}
                 ],
    Ports = [
             #port{
                id=1,
                name="New York",
                docks=['A','B','C','D'],
                container_cap=200
               },
             #port{
                id=2,
                name="San Francisco",
                docks=['A','B','C','D'],
                container_cap=200
               },
             #port{
                id=3,
                name="Miami",
                docks=['A','B','C','D'],
                container_cap=200
               }
            ],
    %% {port, dock, ship}
    Locations = [
                 {1,'B',1},
                 {1, 'A', 3},
                 {3, 'C', 2},
                 {2, 'D', 4},
                 {2, 'B', 5}
                ],
    Ship_Inventory = #{
      1=>[14,15,9,2,6],
      2=>[1,3,4,13],
      3=>[],
      4=>[2,8,11,7],
      5=>[5,10,12]},
    Port_Inventory = #{
      1=>[16,17,18,19,20],
      2=>[21,22,23,24,25],
      3=>[26,27,28,29,30]
     },
    #shipping_state{ships = Ships, containers = Containers, ports = Ports, ship_locations = Locations, ship_inventory = Ship_Inventory, port_inventory = Port_Inventory}.
