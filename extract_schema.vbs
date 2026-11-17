' extract_schema.vbs  -  dumps tables, fields, indexes, relations and queries of an Access DB
' Usage:  cscript //nologo extract_schema.vbs "C:\path\salaires.mdb" Mus_lml
' Output: schema.txt (readable)  +  queries.sql  +  schema_tables.csv  in the current folder
' NOTE: on 64-bit Windows with 32-bit Jet, run with:  C:\Windows\SysWOW64\cscript.exe //nologo ...

Option Explicit
Dim args, dbPath, pwd, eng, db, fso, out, qOut, cOut
Set args = WScript.Arguments
If args.Count < 1 Then
  WScript.Echo "Usage: cscript //nologo extract_schema.vbs <db file> [password]"
  WScript.Quit 1
End If
dbPath = args(0)
If args.Count > 1 Then pwd = args(1) Else pwd = ""

Function OpenDb()
  Dim progs, p, conn
  progs = Array("DAO.DBEngine.120", "DAO.DBEngine.36")
  conn = ";PWD=" & pwd
  For Each p In progs
    On Error Resume Next
    Err.Clear
    Set eng = CreateObject(p)
    If Err.Number = 0 Then
      Set db = eng.OpenDatabase(dbPath, False, True, conn)
      If Err.Number = 0 Then
        WScript.Echo "Connected using " & p
        Set OpenDb = db
        On Error GoTo 0
        Exit Function
      Else
        WScript.Echo p & " failed: " & Err.Description
      End If
    End If
    On Error GoTo 0
  Next
  WScript.Echo "Could not open database."
  WScript.Quit 2
End Function

Function TypeName2(t)
  Select Case t
    Case 1: TypeName2 = "Yes/No"
    Case 2: TypeName2 = "Byte"
    Case 3: TypeName2 = "Integer"
    Case 4: TypeName2 = "Long"
    Case 5: TypeName2 = "Currency"
    Case 6: TypeName2 = "Single"
    Case 7: TypeName2 = "Double"
    Case 8: TypeName2 = "Date/Time"
    Case 10: TypeName2 = "Text"
    Case 11: TypeName2 = "OLE Object"
    Case 12: TypeName2 = "Memo"
    Case 15: TypeName2 = "ReplicationID"
    Case 20: TypeName2 = "Decimal"
    Case Else: TypeName2 = "Type" & t
  End Select
End Function

Function QType(t)
  Select Case t
    Case 0: QType = "SELECT"
    Case 16: QType = "CROSSTAB"
    Case 32: QType = "DELETE"
    Case 48: QType = "UPDATE"
    Case 64: QType = "APPEND"
    Case 80: QType = "MAKE-TABLE"
    Case 96: QType = "DDL"
    Case 112: QType = "PASS-THROUGH"
    Case 128: QType = "UNION"
    Case Else: QType = "Type" & t
  End Select
End Function

Set fso = CreateObject("Scripting.FileSystemObject")
Set out = fso.CreateTextFile("schema.txt", True, True)
Set qOut = fso.CreateTextFile("queries.sql", True, True)
Set cOut = fso.CreateTextFile("schema_tables.csv", True, True)
cOut.WriteLine "table;field;type;size;required;default;primary_key"

Set db = OpenDb()
Dim td, fld, idx, rel, qd, i, f, pk, names, rc

out.WriteLine "DATABASE: " & dbPath
out.WriteLine String(70, "=")
out.WriteLine "TABLES"
out.WriteLine String(70, "=")
For Each td In db.TableDefs
  If (td.Attributes And &H80000002) = 0 Then   ' skip system tables
    rc = "?"
    On Error Resume Next
    rc = td.RecordCount
    On Error GoTo 0
    out.WriteLine ""
    out.WriteLine "TABLE " & td.Name & "   (rows: " & rc & ")" & IIf2(td.Connect <> "", "  [LINKED: " & td.Connect & "]", "")
    ' primary key field names
    pk = "|"
    For Each idx In td.Indexes
      If idx.Primary Then
        For Each f In idx.Fields : pk = pk & f.Name & "|" : Next
      End If
    Next
    For Each fld In td.Fields
      out.WriteLine "   - " & fld.Name & " : " & TypeName2(fld.Type) & IIf2(fld.Type = 10, "(" & fld.Size & ")", "") & _
        IIf2(fld.Required, " NOT NULL", "") & IIf2(InStr(pk, "|" & fld.Name & "|") > 0, " [PK]", "") & _
        IIf2(fld.DefaultValue <> "", " DEFAULT " & fld.DefaultValue, "")
      cOut.WriteLine td.Name & ";" & fld.Name & ";" & TypeName2(fld.Type) & ";" & fld.Size & ";" & fld.Required & ";" & fld.DefaultValue & ";" & (InStr(pk, "|" & fld.Name & "|") > 0)
    Next
    For Each idx In td.Indexes
      names = ""
      For Each f In idx.Fields : names = names & f.Name & ", " : Next
      out.WriteLine "   * INDEX " & idx.Name & " (" & names & ")" & IIf2(idx.Primary, " PRIMARY", "") & IIf2(idx.Unique, " UNIQUE", "")
    Next
  End If
Next

out.WriteLine ""
out.WriteLine String(70, "=")
out.WriteLine "RELATIONS"
out.WriteLine String(70, "=")
For Each rel In db.Relations
  names = ""
  For Each f In rel.Fields : names = names & f.ForeignName & "->" & f.Name & " " : Next
  out.WriteLine rel.Name & ": " & rel.ForeignTable & " (FK) -> " & rel.Table & " (PK)   [" & Trim(names) & "]  attrs=" & rel.Attributes & _
    IIf2((rel.Attributes And 256) <> 0, " CASCADE-UPDATE", "") & IIf2((rel.Attributes And 4096) <> 0, " CASCADE-DELETE", "")
Next

out.WriteLine ""
out.WriteLine String(70, "=")
out.WriteLine "QUERIES (SQL saved in queries.sql)"
out.WriteLine String(70, "=")
For Each qd In db.QueryDefs
  If Left(qd.Name, 1) <> "~" Then
    out.WriteLine qd.Name & "  [" & QType(qd.Type) & "]"
    qOut.WriteLine "-- ========== " & qd.Name & "  [" & QType(qd.Type) & "] =========="
    qOut.WriteLine qd.SQL
    qOut.WriteLine ""
  End If
Next

out.Close : qOut.Close : cOut.Close
db.Close
WScript.Echo "Done. Files written: schema.txt, queries.sql, schema_tables.csv"

Function IIf2(c, a, b)
  If c Then IIf2 = a Else IIf2 = b
End Function
