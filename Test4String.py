# # ============================================================
# # Kid
# # ============================================================
# class Kid:
#     def __init__(self, id) -> None:
#         self.id = id
#         self.left_hand: Kid = None
#         self.right_hand: Kid = None


# # ============================================================
# # Circle
# # ============================================================
# class Circle:
#     def __init__(self, count) -> None:
#         self.head: Kid = None
#         self.tail: Kid = None

#         for i in range(count):
#             self.add_kid(Kid(i + 1))

#     # ==================================================
#     # add a kid always after tail
#     # ==================================================
#     def add_kid(self, kid: Kid) -> None:
#         if self.head is None:
#             # case: if there is no any kids
#             self.head = kid
#             self.tail = kid
#             kid.left_hand = self.head
#             kid.right_hand = self.tail

#         else:
#             self.head.right_hand = kid
#             self.tail.left_hand = kid
#             kid.left_hand = self.head
#             kid.right_hand = self.tail
#             # update tail info
#             self.tail = kid

#     # ==================================================
#     # remove a kid from cricle
#     # ==================================================
#     def remove_kid(self, kid: Kid):
#         kid0 = kid.left_hand
#         kid1 = kid.right_hand

#         if kid is self.head:
#             self.head = kid0
#         if kid is self.tail:
#             self.tail = kid1

#         kid0.right_hand = kid1
#         kid1.left_hand = kid0

#         kid.left_hand = None
#         kid.right_hand = None


# # ============================================================
# # Test
# # ============================================================
# if __name__ == "__main__":
#     circle = Circle(500)

#     step = 0
#     cur_kid = circle.tail
#     last_kid = None
#     while circle.head is not circle.tail:
#         step += 1
#         cur_kid = cur_kid.left_hand

#         if step % 3 == 0:
#             print('========== ========== ========== ========== ========== ==========')
#             print('before operation: last id: {}, cur id: {}, next id: {}'.format(
#                 cur_kid.right_hand.id, cur_kid.id, cur_kid.left_hand.id))
#             # get the last one
#             last_kid = cur_kid.right_hand
#             # remove current
#             circle.remove_kid(cur_kid)
#             # using last as current
#             cur_kid = last_kid

#             print('after operation: last id: {}, cur id: {}, next id: {}'.format(
#                 cur_kid.right_hand.id, cur_kid.id, cur_kid.left_hand.id))

#     print(circle.head.id)

circle = [i for i in range(1, 501)]
step = 0
while len(circle) > 1:
    dels = []
    for kid in circle:
        step += 1
        if step % 3 == 0:
            dels.append(kid)

    for kid in dels:
        circle.remove(kid)
    # cycle = [i for i in cycle if i not in dels]

print(circle)