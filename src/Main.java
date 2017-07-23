public class Main {
	public static int[][] board = new int[8][8];
	
	public static void main(String[] args) {
		setDefaultBoard();
		Board b = new Board();
		b.drawBoard(board);
	}

//	private static int[][] setEmpty(int[][] array) {
//		for(int i = 0; i < 8; i++){
//			for(int j = 0; j < 8; j++){
//				array[i][j] = 0;
//			}
//		}
//		return array;
//	}
	
	
	//setDefaultBoard: reinitializes board array with starting positions.
	private static void setDefaultBoard(){
		for(int i = 0; i < 8; i ++){
			board[i][1] = 1; //set pawns
			board[i][6] = -1;
		}
		//rooks
		board[0][0] = 5;
		board[7][0] = 5;
		
		board[0][7] = -5;
		board[7][7] = -5;
		
		//knights
		board[6][0] = 4;
		board[1][0] = 4;
		
		board[6][7] = -4;
		board[1][7] = -4;
		
		//bishops
		board[5][0] = 3;
		board[2][0] = 3;
		
		board[5][7] = -3;
		board[2][7] = -3;
		
		//queens
		board[4][0] = 9;
		board[4][7] = -9;
		
		//kings
		board[3][0] = 10;
		board[3][7] = -10;
		
	}
	
}
