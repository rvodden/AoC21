import pandas as pd


class Bingo:

    @staticmethod
    def bingo(sequence, boards):
        winning_board = None
        df = Bingo._init_boards(boards)
        idx = pd.IndexSlice
        for value in sequence:
            mask = df.loc[:, idx[:, "value"]] == value
            df.loc[:, idx[:, "marked"]] |= mask.values
            if winning_board := Bingo._winning_board(df):
                board = df.loc(axis=1)[winning_board]
                return Bingo._evaluate_board(board, value)
        return None

    @staticmethod
    def bingo_last_board(sequence, boards):
        winning_value = None
        df = Bingo._init_boards(boards)
        idx = pd.IndexSlice
        for value in sequence:
            if df.empty:
                break
            mask = df.loc[:, idx[:, "value"]] == value
            df.loc[:, idx[:, "marked"]] = df.loc[:, idx[:, "marked"]] | mask.values
            number_dropped = 0
            while (winning_board := Bingo._winning_board(df)) is not None:
                number_dropped += 1
                board = df.loc(axis=1)[winning_board]
                winning_value = Bingo._evaluate_board(board, value)
                df.drop([winning_board], axis=1, inplace=True)
                assert winning_board not in df.columns
        return winning_value

    @staticmethod
    def _init_boards(boards: list[list[int]]) -> pd.DataFrame:
        v_index = pd.MultiIndex.from_product([range(1, 6), range(1, 6)], names=["row", "column"])
        h_index = pd.MultiIndex.from_product([range(len(boards)), ["value", "marked"]], names=["board", "dim"])
        df = pd.DataFrame(index=v_index, columns=h_index)
        for i, board in enumerate(boards):
            df[(i, 'value')] = pd.Series(board, index=v_index)
        idx = pd.IndexSlice
        df.loc[:, idx[:, "marked"]] = False
        return df

    @staticmethod
    def _winning_board(df):
        idx = pd.IndexSlice
        if df.empty:
            return None
        for i in range(1, 6):
            row_wins = df.loc[idx[idx[:, i], idx[:, 'marked']]].all()
            row_wins.index = row_wins.index.droplevel('dim')
            column_wins = df.loc[idx[idx[i, :], idx[:, 'marked']]].all()
            column_wins.index = column_wins.index.droplevel('dim')
            if row_wins.any():
                return row_wins[row_wins].index[0]

            if column_wins.any():
                return column_wins[column_wins].index[0]
        return None

    @staticmethod
    def _evaluate_board(board, value):
        score = value * board[board['marked'] == False]['value'].sum()
        return score
