var 
I : integer;
begin
  I:=0;
  while I<10 do
    begin
    Inc(I);
    if I>5 then
    begin
      break;
    end;
    Writeln (i);
    end;
  I:=0;
  repeat
  begin
    Inc(I);
    if I>5 then
    begin
      break;
    end;
    Writeln (i);
  end;
  until I>=10;
  for I:=1 to 10 do
    begin
    if I>5 then
    begin
      continue;
    end;
    Writeln (i);
    end;
end.