import unittest


class Test(unittest.TestCase):
    def test_1(self):
        input1 = ''
        ordered1 = order(input1)
        self.assertEquals(ordered1, '')

    def test_2(self):
        input2 = 'a=>'
        ordered2 = order(input2)
        self.assertEquals(ordered2, 'a')

    def test_3(self):
        input3 = 'a=>,b=>,c=>'
        ordered3 = order(input3)
        set3 = 'abc'
        self.assertEquals(len(ordered3), 3)
        self.assertTrue(all([j in set3 for j in ordered3]))
        self.assertTrue(all([j in ordered3 for j in set3]))

    def test_4(self):
        input4 = 'a=>,b=>c,c=>'
        ordered4 = order(input4)
        set4 = 'abc'
        self.assertEquals(len(ordered4), 3)
        self.assertTrue(all([j in set4 for j in ordered4]))
        self.assertTrue(all([j in ordered4 for j in set4]))
        self.assertTrue(ordered4.index('c') < ordered4.index('b'))

    def test_5(self):
        input5 = 'a=>,b=>c,c=>f,d=>a,e=>b,f=>'
        ordered5 = order(input5)
        set5 = 'abcdef'
        self.assertEquals(len(ordered5), 6)
        self.assertTrue(all([j in set5 for j in ordered5]))
        self.assertTrue(all([j in ordered5 for j in set5]))
        self.assertTrue(ordered5.index('c') < ordered5.index('b'))
        self.assertTrue(ordered5.index('f') < ordered5.index('c'))
        self.assertTrue(ordered5.index('a') < ordered5.index('d'))
        self.assertTrue(ordered5.index('b') < ordered5.index('e'))

    def test_6(self):
        input6 = 'a=>,b=>,c=>c'
        self.assertRaises(SelfReferencingError, order, input6)

    def test_7(self):
        input7 = 'a=>,b=>c,c=>f,d=>a,e=>,f=>b'
        self.assertRaises(CircularDependencyError, order, input7)

    def test_8(self):
        input8 = 'a=>,b=>c,c=>d,d=>a,e=>,f=>b'
        ordered8 = order(input8)
        set8 = 'abcdef'
        self.assertEquals(len(ordered8), 6)
        self.assertTrue(all([j in set8 for j in ordered8]))
        self.assertTrue(all([j in ordered8 for j in set8]))
        self.assertTrue(ordered8.index('c') < ordered8.index('b'))
        self.assertTrue(ordered8.index('d') < ordered8.index('c'))
        self.assertTrue(ordered8.index('a') < ordered8.index('d'))
        self.assertTrue(ordered8.index('b') < ordered8.index('f'))

    def test_path(self):
        d = {'a': 'b', 'b': 'c', 'c': ''}
        self.assertEquals(path('a', d), 'cb')
        self.assertEquals(path('b', d), 'c')
        self.assertEquals(path('c', d), '')
        d2 = {'a': 'b', 'b': 'c', 'c': 'c'}
        self.assertRaises(SelfReferencingError, path, 'a', d2)


def order(jobs):
    d = make_hash(jobs)
    paths = []
    for i in d:
        paths.append(path(i, d))
    paths.sort(key=len)
    paths.reverse()
    order = ''
    for p in paths:
        order += p if p not in order else ''
    for j in d:
        order += j if j not in order else ''
    return order


def make_hash(jobs):
    jobs = jobs.replace('=>', '').split(',')
    d = {}

    # make dictionary {job:dep}
    for job in jobs:
        if len(job) > 0:
            d[job[0]] = job[1] if len(job) > 1 else ''
    return  d


def path(j, d):
    job = j
    deps = ''
    while len(job) > 0:
        if job == d[job]:
            raise SelfReferencingError
        job = d[job]
        deps += job
        if job == j:
            raise CircularDependencyError
    return deps[::-1]


class SelfReferencingError(Exception):
    def __str__(self):
        return "Jobs cannot depend on themselves"


class CircularDependencyError(Exception):
    def __str__(self):
        return "Jobs cannot have circular dependencies"


if __name__ == '__main__':
    unittest.main()
