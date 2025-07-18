import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.init_ui()

    def init_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for row in range(9):
            for col in range(9):
                e = tk.Entry(frame, width=2, font=('Arial', 18), justify='center', borderwidth=2, relief='ridge')
                e.grid(row=row, column=col, padx=1, pady=1)
                self.entries[row][col] = e

        solve_button = tk.Button(self.root, text="Solve", command=self.solve, font=('Arial', 14), bg='green', fg='white')
        solve_button.pack(pady=10)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_board, font=('Arial', 14), bg='red', fg='white')
        clear_button.pack()

    def get_board(self):
        board = []
        for row in range(9):
            board_row = []
            for col in range(9):
                val = self.entries[row][col].get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    board_row.append(int(val))
                else:
                    board_row.append(0)
            board.append(board_row)
        return board

    def set_board(self, board):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                if board[row][col] != 0:
                    self.entries[row][col].insert(0, str(board[row][col]))

    def clear_board(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

    def solve(self):
        board = self.get_board()
        if self.solve_sudoku(board):
            self.set_board(board)
        else:
            messagebox.showerror("Error", "No solution exists!")

    # Backtracking solver
    def solve_sudoku(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def is_valid(self, board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False

        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[startRow + i][startCol + j] == num:
                    return False

        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
