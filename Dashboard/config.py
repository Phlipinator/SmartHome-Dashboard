class Config:
    """
    A class that stores the configuration settings for the Smart Home Dashboard.

    Attributes:
        adjustmentTable (list): Stores adjustments for each tile in the format (row, column).
        tileList (list): Stores the voltage values for each tile.
        rowList (list): Stores the voltage values for each row.
        colList (list): Stores the voltage values for each column.
        proxyList (list): Stores the proxy information in the format (x, y, State).
    """

    def __init__(self):
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

        self.tileList = [
            # Row 1
            (5.26, 4),
            (4.57, 3),
            (4.25, 2),
            (3.85, 1),
            # Row 2
            (3.51, 5),
            (3.19, 6),
            (2.86, 7),
            (2.54, 8),
            # Row 3
            (2.30, 12),
            (1.98, 11),
            (1.67, 10),
            (1.36, 9),
            # Row 4
            (1.07, 13),
            (0.76, 14),
            (0.45, 15),
            (0.06, 16),
        ]

        self.rowList = [
            (5.1, 1),
            (3.6, 2),
            (2.2, 3),
            (0.7, 4),
        ]

        self.colList = [
            (4.4, 1),
            (2.9, 2),
            (1.5, 3),
            (0.2, 4),
        ]
