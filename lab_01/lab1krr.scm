(define nodup
    (lambda (l)
        (if (null? l)
            '()
            (if (member (car l) (cdr l))
                (nodup (cdr l))
                (cons (car l) (nodup (cdr l)))
                ))))

(nodup '(1 2 4 2 3))
(nodup '(1 1 2 3 1 1 2 3 1 5 7 9 9))

; insereaza un numar intr-o lista in functie
; de un comparator
(define insert
  (lambda (comp x l)
    (if (null? l)
        (list x)
        (let ((first_element (car l))
              (rest (cdr l)))
          (if (comp x first_element)
              (cons x l)
              (cons first_element (insert comp x rest)))))))

(define isortc
  (lambda (comp l)
    (if (null? l)
        '()
        (insert comp (car l) (isortc comp (cdr l))))))

(display '(isort cresc))
(isortc < '(1 4 2 8 5 3))
(display '(isort descresc))
(isortc > '(1 4 2 8 5 3))

; verifica daca un numar este prim
(define is_number_prime
  (lambda (x n)
    (if (> n (integer-sqrt x))
        #t
        (if (= (modulo x n) 0)
            #f
            (is_number_prime x (+ n 1))))))

; wrapper pentru functia care verifica daca un
; numar este prim. Ii mai trimite inca un parametru
; ca argument
(define is_prime
  (lambda (x)
    (if (or (= x 1) (< x 0))
        #f
        (is_number_prime x 2))))


; intoarce toate numerele prime din intervalul a .. b
(define primes
  (lambda (a b)
    (if (> a b)
        '()
        (if (is_prime a) 
            (cons a (primes (+ a 1) b))
            (primes (+ a 1) b )))))

(primes 1 20)

; determina descompunerea unui numar in factori primi
(define desc
  (lambda (x)
    (desc_wrapper x 2)))
  

; wrapper ptr functia desc
(define desc_wrapper
  (lambda (x n)
    (if (= x 1)
        '()
        (if (= (modulo x n) 0)
            (cons n (desc_wrapper (/ x n) n))
            (desc_wrapper x (+ n 1))))))

(desc 12); -> (2 2 3)
(desc 7); -> (7)
(desc 1993)
