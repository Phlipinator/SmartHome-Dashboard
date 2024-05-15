class Config:
    def __init__(self):
        # Stores adjustments for each tile in the format (row, column)
        self.adjustmentTable = [
            # Row 1
            (0, 0),  # Tile 1
            (0, 4),  # Tile 2
            (0, 8),  # Tile 3
            (0, 12),  # Tile 4
            # Row 2
            (4, 0),  # Tile 5
            (4, 4),  # Tile 6
            (4, 8),  # Tile 7
            (4, 12),  # Tile 8
            # Row 3
            (8, 0),  # Tile 9
            (8, 4),  # Tile 10
            (8, 8),  # Tile 11
            (8, 12),  # Tile 12
            # Row 4
            (12, 0),  # Tile 13
            (12, 4),  # Tile 14
            (12, 8),  # Tile 15
            (12, 12),  # Tile 16
        ]

        # Stores the voltage values for each tile
        self.tileList = [
            # Row 1
            (5.0, 4),
            (4.4, 3),
            (4.0, 2),
            (3.64, 1),
            # Row 2
            (3.3, 5),
            (3.0, 6),
            (2.68, 7),
            (2.36, 8),
            # Row 3
            (2.0, 12),
            (1.8, 11),
            (1.5, 10),
            (1.22, 9),
            # Row 4
            (0.94, 13),
            (0.66, 14),
            (0.38, 15),
            (0.1, 16),
        ]

        # Stores the voltage values for each row
        self.rowList = [
            (5.1, 1),
            (3.6, 2),
            (2.2, 3),
            (0.7, 4),
        ]

        # Stores the voltage values for each column
        self.colList = [
            (4.4, 1),
            (2.9, 2),
            (1.5, 3),
            (0.2, 4),
        ]

        self.thresholds = {"tile": 0.15, "row": 0.5, "col": 0.5}
