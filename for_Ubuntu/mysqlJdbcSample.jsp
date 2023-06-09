<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR" %>
<%@ page import = "java.sql.*" %>
<!-- JSP에서 JDBC의 객체를 사용하기 위해 java.sql 패키지를 import 한다 -->

<html>
<head></head>
<body>
<table width="550" border="1">
  
<%
        Connection conn = null;                                        // null로 초기화 한다.
        Statement stmt  = null;
        ResultSet rs    = null;

try{

        String url = "jdbc:mysql://db-gsj7n.vpc-cdb.ntruss.com:3306/test";        // 사용하려는 데이터베이스명을 포함한 URL 기술
        String id = "test";                                                    // 사용자 계정
        String pw = "qwer1234!";                                                // 사용자 계정의 패스워드

        Class.forName("com.mysql.jdbc.Driver");                       // 데이터베이스와 연동하기 위해 DriverManager에 등록한다.
        conn = DriverManager.getConnection(url,id,pw);              // DriverManager 객체로부터 Connection 객체를 얻어온다.
        stmt = conn.createStatement();

        String sql = "SELECT * FROM USER";                        // sql 쿼리
        
        rs = stmt.executeQuery(sql);

while(rs.next()){                                                        // 결과를 한 행씩 돌아가면서 가져온다.

        int aa_id = rs.getInt("ID");
        String aa_name = rs.getString("NAME");
        String aa_ip = rs.getString("IP");
        String aa_cacheid = rs.getString("CACHEID");
%>


<tr style="text-align:center;">
        <td width="100">ID</td>
        <td width="100">NAME</td>
          <td width="100">IP</td>
        <td width="100">CACHEID</td>
</tr>
<tr style="text-align:center;">
        <td width="100"><%=aa_id%></td>
        <td width="100"><%=aa_name%></td>
        <td width="100"><%=aa_ip%></td>
        <td width="100"><%=aa_cacheid%></td>
</tr>

<%

}

}catch(SQLException se) {

        se.printStackTrace();
        out.println("111");

}catch(Exception e){                                                    // 예외가 발생하면 예외 상황을 처리한다.

        e.printStackTrace();
        out.println("member 테이블 호출에 실패했습니다.");

}finally{                                                            // 쿼리가 성공 또는 실패에 상관없이 사용한 자원을 해제 한다.  (순서중요)

        if(rs != null) try{rs.close();}catch(SQLException sqle){}            // Resultset 객체 해제
        if(stmt != null) try{stmt.close();}catch(SQLException sqle){}   // PreparedStatement 객체 해제
        if(conn != null) try{conn.close();}catch(SQLException sqle){}   // Connection 해제

}

%>

</table>
</body>
</html>
