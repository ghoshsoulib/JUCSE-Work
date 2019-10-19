package com.shopping;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class ForgotPassServlet
 */
@WebServlet(name = "forgot", urlPatterns = { "/forgot" })
public class ForgotPassServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
	private String dburl,dbuname,dbpass;
    /**
     * @see HttpServlet#HttpServlet()
     */
    public ForgotPassServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see Servlet#init(ServletConfig)
	 */
	public void init(ServletConfig config) throws ServletException {
		// TODO Auto-generated method stub
		super.init(config);
		dburl=getServletContext().getInitParameter("dburl");
    	dbuname=getServletContext().getInitParameter("dbuname");
    	dbpass=getServletContext().getInitParameter("dbpass");
    	
    	System.out.println(dburl);
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		String uname=request.getParameter("username");
		String password=request.getParameter("password");
		
		DAO dao=new DAO(dburl,dbuname,dbpass);
		PrintWriter out = response.getWriter();
		//Check if username in database
		try {
			if(dao.checkUname(uname))
			{
				dao.updatePass(uname, password);
				response.sendRedirect("index.html");
			}
			else
			{
				out.println("<script type='text/javascript'>");
				out.println("alert('Sorry!! Not a registered user');");
				out.println("</script>");
				
				RequestDispatcher rd=request.getRequestDispatcher("index.html");  
		        rd.include(request, response);
		        
		        return;
			}
		} 
		catch (Exception e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
	}

}