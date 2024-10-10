class A:
    password = 123


class B(A):

    def print_pass(self):
        print(self.password)


b = B()

b.print_pass()