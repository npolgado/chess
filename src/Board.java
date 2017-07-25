import java.awt.Color;
import java.awt.Image;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

import javax.imageio.ImageIO;
import javax.swing.*;

public class Board {
	
	private static ArrayList<Piece> board = new ArrayList<>();
	private int WIDTH = 800;
	private int HEIGHT = 800;
	private int OFFSETHEIGHT = 25;
	JFrame frame;
	Piece movingPiece;
	Piece destinationPiece;
	boolean isSecond = false;
	
	public Board() {
		frame = new JFrame ("Chess");
		frame.setSize(WIDTH, HEIGHT + OFFSETHEIGHT);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		movingPiece = null;
		destinationPiece = null;
	}
	
	public static void main(String[] args) {		
		Board b = new Board();
		b.setDefaultBoard(board);
	}
	
	//move: takes the moving piece, the destination piece, and the board, and moves coords, color, and pieceType
	//	of the moving piece to the destination piece, then sets the piece in the array where the moving piece was to an empty space.
//	public ArrayList<Piece> move(Piece oldSpace, Piece destination, ArrayList<Piece> board){
//		for (Piece piece : board) {
//			if(piece.x == oldSpace.x && piece.y == oldSpace.y && piece.color == oldSpace.color && piece.type == oldSpace.type)
//			{
//				//board.set(board.indexOf(toHere), thisOne);				
//				board.get(board.indexOf(oldSpace)).color = Color.BLUE;
//				board.get(board.indexOf(oldSpace)).type = pieceType.EMPTY;
//				board.get(board.indexOf(oldSpace)).x = oldSpace.x;
//				board.get(board.indexOf(oldSpace)).y = oldSpace.y;
//				//board.set(board.indexOf(piece), new Piece(piece.x, piece.y, Color.BLUE, pieceType.EMPTY));
//			}else if(piece.x == destination.x && piece.y == destination.y && piece.color == destination.color && piece.type == destination.type){
//				board.get(board.indexOf(destination)).color = oldSpace.color;
//				board.get(board.indexOf(destination)).type = oldSpace.type;
//			}
//		}
//		drawBoard(board);
//		return board;
//	}
	
	//setDefaultBoard: takes arraylist of the board and clears it, then add's the default start to the game
	public void setDefaultBoard(ArrayList<Piece> board){
		board.clear();
		board.add(0, new Piece(0, 0, Color.BLACK, pieceType.ROOK, 0));
		board.add(1, new Piece(7, 0, Color.BLACK, pieceType.ROOK, 1));
		board.add(2, new Piece(1, 0, Color.BLACK, pieceType.KNIGHT, 2));
		board.add(3, new Piece(6, 0, Color.BLACK, pieceType.KNIGHT, 3));
		board.add(4, new Piece(2, 0, Color.BLACK, pieceType.BISHOP, 4));
		board.add(5, new Piece(5, 0, Color.BLACK, pieceType.BISHOP, 5));
		board.add(6, new Piece(3, 0, Color.BLACK, pieceType.QUEEN, 6));
		board.add(7, new Piece(4, 0, Color.BLACK, pieceType.KING, 7));
		
		for (int i = 0; i < 8; i++) {
			board.add((2*i) + 8, new Piece(i, 1, Color.BLACK, pieceType.PAWN, (2*i) + 8));
			board.add((2*i) + 9, new Piece(i, 6, Color.WHITE, pieceType.PAWN, (2*i) + 9));
		}
		
		board.add(24, new Piece(0, 7, Color.WHITE, pieceType.ROOK, 24));
		board.add(25, new Piece(7, 7, Color.WHITE, pieceType.ROOK, 25));
		board.add(26, new Piece(1, 7, Color.WHITE, pieceType.KNIGHT, 26));
		board.add(27, new Piece(6, 7, Color.WHITE, pieceType.KNIGHT, 27));
		board.add(28, new Piece(2, 7, Color.WHITE, pieceType.BISHOP, 28));
		board.add(29, new Piece(5, 7, Color.WHITE, pieceType.BISHOP, 29));
		board.add(30, new Piece(3, 7, Color.WHITE, pieceType.QUEEN, 30));
		board.add(31, new Piece(4, 7, Color.WHITE, pieceType.KING, 31));
		
		int num = 32;
		for (int j = 2; j < 6; j++) {
			for (int i = 0; i < 8; i++) {
				board.add(num, new Piece(i, j, Color.BLUE, pieceType.EMPTY, num));
				num++;
			}
		}
		this.board = board;
		drawBoard(board);
		frame.setVisible(true);
	}
	
	//drawBoard: takes array of currentBoard and adds buttons 
    public void drawBoard(ArrayList<Piece> board) 
    {
    	frame.repaint();
    	for (Piece piece : board) 
    	{
    		createButton(piece);
		}
    	
    	createButton(new Piece(0,0,Color.black,null,100));//fuker button
	}
    
    
    /*
     Needed Comment
   
    int count = 0;
	int secCount = 0;
	for (int a = 0; a < ar.length; a++) {
		for (int z = 0; z < ar.length; z++) {
			JButton button = new JButton(Integer.toString(ar[z][a]));
			button.setBounds(new Rectangle( ((WIDTH/8)*z), ((HEIGHT/8)*a), WIDTH/8, HEIGHT/8) );
			button.setOpaque(true);
			button.setBorderPainted(false);
			button.addActionListener(new EndingListener ());
			
			if (secCount % 8 == 0)
			{
				count ++;
			}
			//new new new shit
			
			if (count % 2 == 0)
			{
				button.setBackground (new Color (172, 112, 61));
			}
			frame.add(button);
			count ++;
			secCount++;
		}
	}    
	
	//if ur reading this, stay woke lil fuker
	JButton fuker = new JButton ();
	frame.add(fuker);
	frame.setVisible(true);
	*/
    
    //createButton: takes piece and draws it on the board
    private void createButton(Piece p) {
    	ButtonExtend button;
    	if(p.type == null)
    	{
    		button = new ButtonExtend();
    	}
    	else if (p.type.equals(pieceType.EMPTY))
    	{
    		button = new ButtonExtend(" - ");
    		button.setActionCommand(p.toString());
    	}
    	else
    	{
    		button = new ButtonExtend(p.type.toString().substring(0,2));
    		button.setActionCommand(p.toString());
   		}
    	button.setPiece(p);
		button.setBounds(((this.WIDTH/8)*p.x), ((this.HEIGHT/8)*p.y), this.WIDTH/8, this.HEIGHT/8);
		button.setOpaque(true);
		button.setBorderPainted(false);
		button.addActionListener(new EndingListener ());
		
		if (p.type != null)
		{
			//adding an image to the button, corresponding to their piece and color
			String img = null;
			switch (p.type)
			{
			case PAWN:
				img = "pawn.png";
				button.addImage (img);
				break;
//			case KNIGHT:
//				img = "knight";
//				break;
//			case BISHOP:
//				img = "bishop";
//				break;
//			case ROOK:
//				img = "rook";
//				break;
//			case QUEEN:
//				img = "queen";
//				break;
//			case KING:
//				img = "king";
//				break;
			default:
				break;
			}
			frame.add(button);
		}
		
		
	}

    private class EndingListener extends Board implements ActionListener
    { 
		public void actionPerformed(ActionEvent e) 
		{
			int indexOf = Integer.parseInt(e.getActionCommand());
			if(isSecond == false && board.get(indexOf).type != pieceType.EMPTY){
				 movingPiece = board.get(indexOf);
				 isSecond = true;
			}
			else if(isSecond == true)
			{
				 destinationPiece = board.get(indexOf);
				 movingPiece.isLegal(destinationPiece, board);
				 isSecond = false;
			}
			
		}
    }
	
}
