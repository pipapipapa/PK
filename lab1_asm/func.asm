place_func_ db ?



;Function exit
exit:
    mov rax, 1
    mov rbx, 0
    int 0x80

;Function printing of string
;input rsi - place of memory of begin string
print_str:
    push rax
    push rdi
    push rdx
    push rcx
    mov rax, rsi
    call len_str
    mov rdx, rax
    mov rax, 1
    mov rdi, 1
    syscall
    pop rcx
    pop rdx
    pop rdi
    pop rax
    ret

;The function makes new line
new_line:
   push rax
   push rdi
   push rsi
   push rdx
   push rcx
   mov rax, 0xA
   push rax
   mov rdi, 1
   mov rsi, rsp
   mov rdx, 1
   mov rax, 1
   syscall
   pop rax
   pop rcx
   pop rdx
   pop rsi
   pop rdi
   pop rax
   ret


;The function finds the length of a string
;input rax - place of memory of begin string
;output rax - length of the string
len_str:
  push rdx
  mov rdx, rax
  .iter:
      cmp byte [rax], 0
      je .next
      inc rax
      jmp .iter
  .next:
     sub rax, rdx
     pop rdx
     ret


;Function converting the string to the number
;input rsi - place of memory of begin string
;output rax - the number from the string
str_number:
    push rcx
    push rbx
    push r15

    xor rax,rax
    xor rcx,rcx
    mov r15, 'p'

    cmp byte [rsi], '-'

    je .is_neg




.loop:
    xor     rbx, rbx
    mov     bl, byte [rsi+rcx]
    cmp     bl, 48
    jl      .finished
    cmp     bl, 57
    jg      .finished

    sub     bl, 48
    add     rax, rbx
    mov     rbx, 10
    mul     rbx
    inc     rcx
    jmp     .loop

.finished:
    cmp     rcx, 0
    je      .restore
    mov     rbx, 10
    div     rbx




.restore:
    cmp r15, 'n'
    jne ._posi
    ._nega:
        neg rax
    ._posi:

    pop r15
    pop rbx
    pop rcx
    ret

.is_neg:
    inc rcx
    mov r15, 'n'
    jmp .loop


print_symbl:
     push rbx
     push rdx
     push rcx
     push rax

     push rax
     mov eax, 4
     mov ebx, 1
     pop rdx
     mov [place_func_], dl
     mov ecx, place_func_
     mov edx, 1
     int 0x80
     pop rax
     pop rcx
     pop rdx
     pop rbx
     ret

print_number:
    push rbp
    mov rbp, rsp
    sub rsp, 8
    push rcx
    push rbx

    xor rcx, rcx
    mov rbx, 10

    cmp rax, 0
    jge ._pos
    ._neg:
      neg rax
      push rax
      mov rax, '-'
      call print_symbl
      pop rax

    ._pos:

    .loop:
      xor rdx, rdx
      div rbx
      add rdx, '0'
      push rdx
      inc rcx
      cmp rax, 0
      jne .loop

    .print_digit:
      pop rax
      call print_symbl
      dec rcx
      cmp rcx, 0
      jne .print_digit

    pop rbx
    pop rcx
    add rsp, 8
    mov rsp, rbp
    pop rbp
    ret


;The function realizates user input from the keyboard
;input: rsi - place of memory saved input string
input_keyboard:
  push rax
  push rdi
  push rdx

  mov rax, 0
  mov rdi, 0
  mov rdx, 255
  syscall

  xor rcx, rcx
  .loop:
     mov al, [rsi+rcx]
     inc rcx
     cmp rax, 0xA
     jne .loop

  dec rcx
  mov byte [rsi+rcx], 0

  pop rdx
  pop rdi
  pop rax
  ret

;The function converts the nubmer to string
;input rax - number
;rsi -address of begin of string
number_str:
  push rbx
  push rcx
  push rdx
  xor rcx, rcx
  mov rbx, 10
  .loop_1:
    xor rdx, rdx
    div rbx
    add rdx, 48
    push rdx
    inc rcx
    cmp rax, 0
    jne .loop_1
  xor rdx, rdx
  .loop_2:
    pop rax
    mov byte [rsi+rdx], al
    inc rdx
    dec rcx
    cmp rcx, 0
  jne .loop_2
  mov byte [rsi+rdx], 0
  pop rdx
  pop rcx
  pop rbx
  ret





;;; Программа сравнивает строку по адресу rsi
;;; со строкой по адресу rdi
;;; Если они равны, то rax = 1
;;; Если не равны, то rax = 0
;;; input: rsi, rdi - addresses of strings
;;; output rax = 1|0
equal_string:
	mov rax, rsi
	call len_str
	mov r8,rax
	mov rax, rdi
	call len_str
	mov r9,rax
	cmp r8,r9
	jne l1
	xor rcx, rcx
	xor rax,rax
	inc rax
	xor rdx, rdx
pr:
	mov dl, [rsi+rcx]
	cmp dl, [rdi+rcx]
	jne l1
	inc rcx
	cmp rcx, r8
	jle pr
	ret
l1:
	mov rax, 0
	ret