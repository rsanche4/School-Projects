(** Author: Rafael Sanchez
    I pledge my honor that I have abided by the Stevens Honor System.
    Due: 21 Feb 2021 
	This simple program encodes a mini logo by compressing to a sequence of numbers
	Written for CS 496*)

type program = int list

(** Declaring the letter_e which will be our sample program through out *)
let  letter_e = [0;2;2;3;3;5;5;4;3;5;4;3;3;5;5;1]

(** Implementation of the function 1 *)
let rec mirror_image l =
    match l with
    | [] -> []
    | [1] -> [1]
    | h::t -> if h=0 then h::mirror_image t
              else
                (
                    if h=2 then 4::mirror_image t
                    else if h=4 then 2::mirror_image t
                    else if h=3 then 5::mirror_image t
                    else if h=5 then 3::mirror_image t
                    else mirror_image t
                )

(** Implementation of the function 2 *)
let rec rotate_90_letter l =
    match l with
    | [] -> []
    | [1] -> [1]
    | h::t -> if h=0 then h::rotate_90_letter t
              else
                (
                    if h=2 then 3::rotate_90_letter t
                    else if h=4 then 5::rotate_90_letter t
                    else if h=3 then 4::rotate_90_letter t
                    else if h=5 then 2::rotate_90_letter t
                    else rotate_90_letter t
                )

let rec map (f:'a -> 'b) (l:'a list) : 'b list =
    match l with
    | [] -> []
    | h::t -> f h :: map f t

(** Implementation of the function 3 *)
let rotate_90_word l =
    match l with
    | [] -> []
    | h::t -> map rotate_90_letter l

(** Implementation of the function 4 *)
let rec repeat n x =
    match n with
    | 0 -> []
    | _ -> repeat (n-1) x @ [x]

let rec map2 f l n =
    match l with
    | [] -> []
    | [1] -> [1]
    | h::t -> (f n h) @ map2 f t n

(** Implementation of the function 5 using map *)
let rec pantograph n p =
    match p with
    | [] -> []
    | h::t -> if h=0 then h::pantograph n t
              else 
              (
                  map2 repeat p n
              )

(** Implementation of the function 5 without using map *)
let rec pantograph_nm n p =
    match p with
    | [] -> []
    | h::t -> if h=0 then h::pantograph n t
              else 
              (
                  repeat n h @ pantograph_nm n t 
              )

let rec foldr f l n =
    match l with
    | [] -> []
    | [1] -> [1]
    | h::t -> f h (foldr f t n) n

let append h r n =
    (repeat n h) @ r

(** Implementation of the function 5 using fold *)
let rec pantograph_f n p =
    match p with
    | [] -> []
    | h::t -> if h=0 then h::pantograph n t
              else 
              (
                  foldr append p n
              )

(** Implementation of the function 6 *)
let rec coverage pair l =
    match l with
    | [] -> [pair]
    | [1] -> [pair]
    | h::t -> if h=0 then pair::coverage pair t
              else 
              (
                if h=2 then (fst pair , snd pair + 1)::coverage (fst pair , snd pair + 1) t
                else if h=3 then (fst pair + 1 , snd pair)::coverage (fst pair + 1 , snd pair) t
                else if h=4 then (fst pair , snd pair - 1)::coverage (fst pair , snd pair - 1) t
                else if h=5 then (fst pair - 1 , snd pair)::coverage (fst pair - 1 , snd pair) t
                else coverage pair t
              ) 


let rec times_repeat num l =
    match l with
    | [] -> 0
    | h::t -> if h=num then 1 + times_repeat num t
              else 0

let rec clean l =
    match l with
    | [] -> []
    | h0::h1::t -> if fst h0 = fst h1 then clean (h0::t)
                   else h0::clean (h1::t)
    | _ -> l  

let rec compress' l =
    match l with
    | [] -> []
    | h::t -> (h , times_repeat h l)::compress' t

(** Implementation of the function 7 *)
let compress l =
    match l with
    | [] -> []
    | h::t -> clean (compress' l)

let rec map3 f l =
    match l with
    | [] -> []
    | h::t -> f h @ map3 f t

let rec expand' fir sec =
    match sec with
    | 0 -> []
    | _ -> fir::expand' fir (sec-1)

let expand pair = expand' (fst pair) (snd pair)

(** Implementation of the function 8 using map *)
let rec uncompress_m l =
    match l with
    | [] -> []
    | h::t -> map3 expand l

let appending h r = h @ r 

let rec foldr2 appendin exp l =
    match l with
    | [] -> []
    | h::t -> appendin (exp h) (foldr2 appendin exp t)

(** Implementation of the function 8 using fold *)
let rec uncompress_f l =
    match l with
    | [] -> []
    | h::t -> foldr2 appending expand l

let rec optimize' pen_up l =
    match l with
    | [] -> []
    | [0] -> [0]
    | h::t -> if pen_up && h=1 then optimize' true t
              else if pen_up then h::(optimize' false t)
              else if h=1 then h::(optimize' true t)
              else h::optimize' false t  

(** Implementation of the function 9 *)
let optimize (l:program) : program =
    match l with
    | [] -> []
    | h::t -> optimize' true l