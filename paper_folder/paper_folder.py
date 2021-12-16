import numpy as np


class PaperFolder:

    def count_dots(input_data: list[tuple[int, int]], fold_data: list[tuple[str, int]]):
        return np.count_nonzero(PaperFolder.fold_dots(input_data, fold_data))

    def fold_dots(input_data: list[tuple[int, int]], fold_data: list[tuple[str, int]]):
        dot_coords = np.array(input_data, dtype=int).T
        dot_coords[0, 1] = dot_coords[1, 0]

        max_x = np.max(dot_coords[1])
        max_y = np.max(dot_coords[0])

        dots = np.zeros((max_x + 1, max_y + 1), dtype=int)
        dots[dot_coords[1], dot_coords[0]] = 1
        for axis, fold in fold_data:
            match axis:
                case 'y':
                    dots = PaperFolder._fold_y(dots, fold)
                case 'x':
                    dots = PaperFolder._fold_x(dots, fold)
            
        return dots

    def _fold_y(dots: np.ndarray, fold):
        top = dots[:fold]
        bottom = dots[fold + 1:][::-1]

        len_diff = len(top) - len(bottom)
        if len_diff > 0:
            bottom = np.vstack([np.zeros((len_diff, bottom.shape[1]), dtype=int), bottom])
        elif len_diff < 0:
            print(f"Need to pad top by {len_diff}")
            top = np.vstack([np.zeros((-len_diff, top.shape[1]), dtype=int), top])
        
        return bottom | top 

    def _fold_x(dots: np.ndarray, fold):
        return PaperFolder._fold_y(dots.T, fold).T