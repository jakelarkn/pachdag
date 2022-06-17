import unittest

from dag import DAG, DAGInputError


class DAGTestCase(unittest.TestCase):

    def test_dag_graph_build(self):
        text =   """A:
                    B: A
                    C: B"""

        dag = DAG(text)
        self.assertEqual(dag.graph['A'], [])
        self.assertEqual(dag.graph['B'], ['A'])
        self.assertEqual(dag.graph['C'], ['B'])

    def test_dag_graph_invalid_input_1(self):
        text = """
            A:
            C: B
        """

        with self.assertRaises(DAGInputError) as ctx:
            dag = DAG(text)

        self.assertTrue('node parent has not been declared' in str(ctx.exception))

    def test_dag_graph_invalid_input_2(self):
        text = """
            A:
            C: B
            B: A
        """

        with self.assertRaises(DAGInputError) as ctx:
            dag = DAG(text)

        self.assertTrue('node parent has not been declared' in str(ctx.exception))

    def test_dag_graph_invalid_input_3(self):
        text = """
            A: C
            C: B
            B: A
        """

        with self.assertRaises(DAGInputError) as ctx:
            dag = DAG(text)

        self.assertTrue('node parent has not been declared' in str(ctx.exception))

    def test_dag_graph_invalid_input_4_node_redefintion(self):
        text = """
            A: 
            B:
            C: B
            C: A
        """

        with self.assertRaises(DAGInputError) as ctx:
            dag = DAG(text)

        self.assertTrue('node is defined more than once' in str(ctx.exception))

    def test_dag_graph_invalid_input_4_empty_graph(self):
        text = """
        
        
        
        
        """

        with self.assertRaises(DAGInputError) as ctx:
            dag = DAG(text)

        self.assertTrue('text graph input was empty' in str(ctx.exception))

    def test_dag_graph_invalid_input_4_colon_syntax_error(self):
        text = """
            A: 
            B: A
            C: A :B
        """

        with self.assertRaises(DAGInputError) as ctx:
            dag = DAG(text)

        self.assertTrue('invalid input definition of line' in str(ctx.exception))

    def test_dag_graph_invalid_input_4_colon_syntax_error_2(self):
        text = """
            A: 
            B: A
            C A 
        """

        with self.assertRaises(DAGInputError) as ctx:
            dag = DAG(text)

        self.assertTrue('invalid input definition of line' in str(ctx.exception))

    def test_dag_in_out_degrees(self):

        text =   """A:
                    B: A
                    C: B"""

        dag = DAG(text)
        self.assertEqual(dag.in_degree['A'], 1)
        self.assertEqual(dag.out_degree['A'], 0)

        self.assertEqual(dag.in_degree['B'], 1)
        self.assertEqual(dag.out_degree['B'], 1)

        self.assertEqual(dag.in_degree['C'], 0)
        self.assertEqual(dag.out_degree['C'], 1)

        self.assertEqual(len(dag.out_degree), 3)
        self.assertEqual(len(dag.in_degree), 3)

    def test_dag_leaves(self):

        text =   """A:
                    B: A
                    C: B
                    D: B
                    E: B
                    F: A"""

        dag = DAG(text)
        self.assertEqual(dag.leaves(), ['C', 'D', 'E', 'F'])

    def test_dag_leaves_1(self):

        text = """
            A:
            B: A
            C: B
            """

        dag = DAG(text)
        self.assertEqual(dag.leaves(), ['C'])

    def test_dag_leaves_2(self):
        text = """
            A:
            B: A
            C: A
            """

        dag = DAG(text)
        self.assertEqual(dag.leaves(), ['B', 'C'])

    def test_dag_leaves_3(self):
        text = """
            A:
            B: A
            C: A
            D: B, C
            """

        dag = DAG(text)
        self.assertEqual(dag.leaves(), ['D'])

    def test_dag_ancestors(self):
        text = """A:
                B: A
                C: A
                D: B, C"""

        dag = DAG(text)
        self.assertEqual(set(dag.ancestors('A')), {'A'})
        self.assertEqual(set(dag.ancestors('B')), {'A', 'B'})
        self.assertEqual(set(dag.ancestors('C')), {'A', 'C'})
        self.assertEqual(set(dag.ancestors('D')), {'A', 'B', 'C', 'D'})

    def test_dag_ancestors(self):
        text = """
                A:
                B: A
                C: B
                D: B
                E: D
                 
                """

        dag = DAG(text)
        self.assertEqual(set(dag.ancestors('A')), {'A'})
        self.assertEqual(set(dag.ancestors('B')), {'A', 'B'})
        self.assertEqual(set(dag.ancestors('C')), {'A', 'B', 'C'})
        self.assertEqual(set(dag.ancestors('E')), {'A', 'B', 'D', 'E'})

    def test_dag_top_sort(self):
        text = """A:
                B: A
                C: B
                D:
                E: D
                F: C, E
                G: F
                H: G"""

        dag = DAG(text)
        self.assertEqual(dag._top_sort(), ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])

        text2 = """
            A:
            Y: A
            X: A
            D: X, Y
        """
        dag = DAG(text2)
        self.assertEqual(dag._top_sort(), ['A', 'Y', 'X', 'D'])


    def test_dag_bisectors_1(self):
        text = """
            A:
            B: A
            C: A
            D: B, C
        """
        dag = DAG(text)
        self.assertEqual(set(dag.bisectors()), {'B', 'C'})

    def test_dag_bisectors_2(self):
        text = """
            A:
            B: A
            C: B
            D:
            E: D
            F: C, E
            G: F
            H: G
        """
        dag = DAG(text)
        self.assertEqual(set(dag.bisectors()), {'C'})

    # example from the git blog post
    def test_dag_bisectors_3(self):
        text = """
            A:
            B: A
            C: B
            D: C
            E: D
            F: E
            G: F
            H: G
            I: H
            J: I
            K: F
            L: K
            M: L
            N: M
            O: J, N
        
        """
        dag = DAG(text)
        self.assertEqual(set(dag.bisectors()), {'G', 'H', 'K', 'L'})


if __name__ == '__main__':
    unittest.main()
