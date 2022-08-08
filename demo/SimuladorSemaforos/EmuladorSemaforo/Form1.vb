Public Class Form1

    Dim numero_semaf

    Function CrearButton(height As Int16, width As Int16, positiion As Short, texto As String) As Button
        Dim b As New Button()

        b.Text = texto
        b.Height = height
        b.Left = 20
        b.Width = width
        b.Top = (positiion - 1) * (b.Height + 3)
        b.Enabled = False

        If texto = "R" Then
            b.BackColor = Color.Red
        End If

        If texto = "Y" Then
            b.BackColor = Color.Yellow
        End If

        If texto = "G" Then
            b.BackColor = Color.Green
        End If

        Return b

    End Function

    Function CrearSemaforo(height As Int16, width As Int16, positiion As Int16) As Panel
        Dim panal_botones = New Panel()
        panal_botones.Height = height
        panal_botones.Width = width

        Dim red = CrearButton(panal_botones.Height / 3, width, 1, "R")
        Dim yellow = CrearButton(panal_botones.Height / 3, width, 2, "Y")
        Dim green = CrearButton(panal_botones.Height / 3, width, 3, "G")

        panal_botones.Controls.Add(red)
        panal_botones.Controls.Add(yellow)
        panal_botones.Controls.Add(green)

        Return panal_botones
    End Function


    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click

        For I As Integer = 1 To numero_semaf
            'Dim b = CrearButton(Panel1.Height / numero_semaf - 3, Panel1.Width - 20, I, "A")
            Dim new_width = (Panel1.Width - 20) / numero_semaf - 3
            Dim b = CrearSemaforo(Panel1.Height, new_width, I)
            b.Left = (I - 1) * new_width
            Panel1.Controls.Add(b)

            Dim titulo = New TextBox()
            titulo.Text = "Semaforo " & I
            titulo.Left = (I - 1) * (new_width + 10)
            Panel2.Controls.Add(titulo)



        Next I

        Button1.Enabled = False
    End Sub

    Private Sub NumericUpDown1_ValueChanged(sender As Object, e As EventArgs) Handles NumericUpDown1.ValueChanged
        numero_semaf = NumericUpDown1.Value
    End Sub
End Class
