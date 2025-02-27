import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSpinBox, QHBoxLayout, QLineEdit, QDialog, QMessageBox, QFormLayout, QSizePolicy
from PySide6.QtCore import QTimer

from modelos.item_cardapio import Lanche, Bebida, Sobremesa
from modelos.pedido import Pedido

class JanelaAdicionarPedido(QDialog):
    def __init__(self, gerente_pedidos, id_pedido, cliente=False):
        super().__init__()
        self.gerente_pedidos = gerente_pedidos
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.itens_pedido = []
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Adicionar Pedido #{self.id_pedido}")
        self.resize(600, 400)
        
        layout = QVBoxLayout()

        self.label_mesa = QLabel("Número da Mesa:")
        self.input_mesa = QLineEdit()
        mesa_layout = QHBoxLayout()
        mesa_layout.addWidget(self.label_mesa)
        mesa_layout.addWidget(self.input_mesa)
        mesa_layout.setStretchFactor(self.label_mesa, 1)
        mesa_layout.setStretchFactor(self.input_mesa, 3)

        # Atualizar os itens do cardápio
        self.cardapio = [
            ("Burguer Clássico", "Pão artesanal, 2 hamburgueres de com blend de carnes selecionadas, maionese especial, cebola roxa, tomate e alface", 29.90),
            ("Burguer Bacon", "Pão artesanal, 2 hamburgueres de costela, maionese especial, molho barbecue, cebola caramelizada e bacon em fatias", 34.90),
            ("Suco de Laranja 500ml", "Feito somente com laranjas e água, sem açúcar adicional", 7.90),
            ("Coca-Cola 600ml", "Servido em frasco de vidro com limão adicional", 6.90),
            ("Pudim médio", "Pudim caseiro convencional", 12.90),
            ("Petit Gateau", "Petit Gateau clássico, servido com sorvete adicional", 19.90)
        ]

        self.total_label = QLabel("Total: R$ 0.00")
        total_layout = QHBoxLayout()
        total_layout.addStretch(1)
        total_layout.addWidget(self.total_label)

        for item_nome, item_descricao, item_preco in self.cardapio:
            item_layout = QHBoxLayout()
            label_item = QLabel(f"{item_nome} - {item_descricao} - R$ {item_preco:.2f}")
            spinbox_quantidade = QSpinBox()
            spinbox_quantidade.setRange(0, 10)
            spinbox_quantidade.valueChanged.connect(self.atualizar_total)
            item_layout.addWidget(label_item)
            item_layout.addWidget(spinbox_quantidade)
            layout.addLayout(item_layout)
            self.itens_pedido.append((item_nome, item_descricao, item_preco, spinbox_quantidade))
        
        layout.addLayout(total_layout)
        layout.addLayout(mesa_layout)

        self.botao_concluir_pedido = QPushButton("Concluir Pedido")
        self.botao_concluir_pedido.clicked.connect(self.concluir_pedido)
        layout.addWidget(self.botao_concluir_pedido)
        
        container = QWidget()
        container.setLayout(layout)
        self.setLayout(layout)

    def atualizar_total(self):
        total = 0.0
        for item_nome, item_descricao, item_preco, spinbox_quantidade in self.itens_pedido:
            total += item_preco * spinbox_quantidade.value()
        self.total_label.setText(f"Total: R$ {total:.2f}")
    
    def concluir_pedido(self):
        numero_mesa = self.input_mesa.text()
        pedido = Pedido(self.id_pedido, numero_mesa)
        for item_nome, item_descricao, item_preco, spinbox_quantidade in self.itens_pedido:
            quantidade = spinbox_quantidade.value()
            for _ in range(quantidade):
                if "Burguer" in item_nome:
                    item = Lanche(item_nome, item_descricao, item_preco)
                elif "Suco" in item_nome or "Coca" in item_nome:
                    item = Bebida(item_nome, item_descricao, item_preco)
                else:
                    item = Sobremesa(item_nome, item_descricao, item_preco)
                pedido.adicionar_item(item)
        
        pedido_origem = "cliente" if self.cliente else "atendente"
        self.gerente_pedidos.adicionar_pedido(pedido, pedido_origem)

        msg = QMessageBox()
        msg.setWindowTitle("Pedido Concluído")
        msg.setText(f"Pedido {self.id_pedido} realizado com sucesso!")
        QTimer.singleShot(2000, msg.close)
        msg.exec()
        
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    from gerentes.gerente_pedidos import GerentePedidos
    gerente_pedidos = GerentePedidos()
    janela = JanelaCliente(gerente_pedidos)
    janela.show()
    
    sys.exit(app.exec())
