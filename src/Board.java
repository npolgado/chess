import java.awt.Color;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Iterator;

import javax.swing.*;
import javax.swing.border.Border;

public class Board {

	private int WIDTH = 800;
	private int HEIGHT = 800;
	private int OFFSETHEIGHT = 25;
	JFrame frame;
	
	
	public Board() {
		frame = new JFrame ("Chess");
		frame.setSize(WIDTH, HEIGHT + OFFSETHEIGHT);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
	}
	
	
	//setDefaultBoard: takes arraylist of the board and clears it, then add's the default start to the game
	public void setDefaultBoard(ArrayList<Piece> board){
		board.clear();
		board.add(new Piece(0, 0, Color.BLACK, pieceType.ROOK));
		board.add(new Piece(7, 0, Color.BLACK, pieceType.ROOK));
		board.add(new Piece(1, 0, Color.BLACK, pieceType.KNIGHT));
		board.add(new Piece(6, 0, Color.BLACK, pieceType.KNIGHT));
		board.add(new Piece(2, 0, Color.BLACK, pieceType.BISHOP));
		board.add(new Piece(5, 0, Color.BLACK, pieceType.BISHOP));
		board.add(new Piece(3, 0, Color.BLACK, pieceType.QUEEN));
		board.add(new Piece(4, 0, Color.BLACK, pieceType.KING));
		
		for (int i = 0; i < 8; i++) {
			board.add(new Piece(i, 1, Color.BLACK, pieceType.PAWN));
			board.add(new Piece(i, 6, Color.WHITE, pieceType.PAWN));
		}
		
		board.add(new Piece(0, 7, Color.WHITE, pieceType.ROOK));
		board.add(new Piece(7, 7, Color.WHITE, pieceType.ROOK));
		board.add(new Piece(1, 7, Color.WHITE, pieceType.KNIGHT));
		board.add(new Piece(6, 7, Color.WHITE, pieceType.KNIGHT));
		board.add(new Piece(2, 7, Color.WHITE, pieceType.BISHOP));
		board.add(new Piece(5, 7, Color.WHITE, pieceType.BISHOP));
		board.add(new Piece(3, 7, Color.WHITE, pieceType.QUEEN));
		board.add(new Piece(4, 7, Color.WHITE, pieceType.KING));
		
		for (int j = 2; j < 6; j++) {
			for (int i = 0; i < 8; i++) {
				board.add(new Piece(i, j, Color.BLUE, pieceType.EMPTY));
			}
		}
	}
	
	//drawBoard: takes array of currentBoard and adds buttons 
    public void drawBoard(ArrayList<Piece> board) 
    {
    	for (Piece piece : board) 
    	{
    		createButton(piece);
		}
    	createButton(new Piece(0,0,Color.black,null));//fuker button
	}
    
    /*int count = 0;
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
	
	//if ur reading this, stay woke lil fucker
	JButton fuker = new JButton ();
	frame.add(fuker);
	frame.setVisible(true);*/
    
    //createButton: takes piece and draws it on the board
    private void createButton(Piece p) {
    	JButton button;
    	if(p.type == null)
    	{
    		button = new JButton();
    	}
    	else if (p.type.equals(pieceType.EMPTY))
    	{
    		button = new JButton(" - ");
    		button.setActionCommand(p.toString());
    	}
    	else
    	{
    		button = new JButton(p.type.toString().substring(0,2));
    		button.setActionCommand(p.toString());
   		}
    	
		button.setBounds(((this.WIDTH/8)*p.x), ((this.HEIGHT/8)*p.y), this.WIDTH/8, this.HEIGHT/8);
		button.setOpaque(true);
		button.setBorderPainted(false);
		button.addActionListener(new EndingListener ());		
		frame.add(button);
	}

    private class EndingListener implements ActionListener
    {
    	
		public void actionPerformed(ActionEvent e) 
		{
			System.out.println(e.getActionCommand());
		}
    }
	
}
