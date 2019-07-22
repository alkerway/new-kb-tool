from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QScrollArea, QMenu, QAction
from PySide2.QtCore import Qt, SIGNAL
from PySide2.QtGui import QCursor

from .progressbar import ProgressBar
from .transactionline import TransactionLine
from kbwidgets.modals import EditCategoryTotalModal, EditTextModal
from kbutils import clearLayout
from kbstate import Events

class Category(QWidget):
    def __init__(self, name, categoryTotal, transactions, state):
        QWidget.__init__(self)
        self.name = name
        self.state = state
        self.transactions = []
        self.categoryTotal = categoryTotal
        self.collapsed = True

        self.sectionLayout = QVBoxLayout()
        self.gridContainer = QWidget()
        self.transactionArea = QScrollArea()
        self.progressBar = ProgressBar()

        self.addHeader()
        self.addBody(transactions)
        self.setLayout(self.sectionLayout)
        self.setAcceptDrops(True)

    def addHeader(self):
        self.headerText = QLabel()
        self.headerText.setText(self.name)
        # self.headerText.setFont(self.boldFont)
        self.headerText.setCursor(Qt.PointingHandCursor)
        self.headerText.mousePressEvent = self.toggleCollapsed

        self.collapseButton = QLabel()
        self.collapseButton.setText('⊞' if self.collapsed else '⊟')
        self.collapseButton.setMaximumWidth(12)
        self.collapseButton.setCursor(Qt.PointingHandCursor)
        self.collapseButton.setToolTip('collapse')
        self.collapseButton.mousePressEvent = self.toggleCollapsed

        self.progressBar = ProgressBar(self.name == 'Income')
        self.progressBar.setCursor(Qt.PointingHandCursor)
        self.progressBar.mousePressEvent = lambda event: self.promptEditVal(self.name, self.categoryTotal)
        self.progressBar.setToolTip('Edit Max')

        self.uncategorizedAmtDisplay = QLabel()
        self.uncategorizedAmtDisplay.setText('$' + str(self.categoryTotal))
        self.uncategorizedAmtDisplay.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        header = QHBoxLayout()
        header.addWidget(self.collapseButton)
        header.addWidget(self.headerText)

        if self.name != 'Uncategorized':
            header.addWidget(self.progressBar)
            if self.name != 'Income':
                self.headerText.setContextMenuPolicy(Qt.CustomContextMenu)
                self.connect(self.headerText, SIGNAL('customContextMenuRequested(const QPoint &)'), self.titleContextMenu)
        else:
            header.addWidget(self.uncategorizedAmtDisplay)

        self.sectionLayout.addLayout(header)

    def addBody(self, transactions):
        self.transactionGrid = QVBoxLayout()
        self.addTransactions(transactions)

    def addTransactions(self, transactions):
        self.transactions += transactions
        clearLayout(self.transactionGrid)
        self.transactionGrid = QVBoxLayout()

        self.transactions.sort(key=lambda t: t.date)

        for idx, transaction in enumerate(self.transactions):
            line = TransactionLine(transaction)
            line.setContextMenuPolicy(Qt.CustomContextMenu)
            self.connect(line, SIGNAL('customContextMenuRequested(const QPoint &)'),
                         lambda event, t=line: self.lineContextMenu(t))
            line.adjustSize()
            self.transactionGrid.addWidget(line)

        self.gridContainer.deleteLater()
        self.gridContainer = QWidget()
        self.gridContainer.setLayout(self.transactionGrid)

        self.transactionArea.deleteLater()
        self.transactionArea.setParent(None)
        self.transactionArea = QScrollArea()
        self.transactionArea.setWidget(self.gridContainer)
        if self.collapsed:
            self.transactionArea.hide()

        self.sectionLayout.addWidget(self.transactionArea)
        self.sectionLayout.setMargin(0)

        self.updateAmtDisplay()
        # if self.name != 'Uncategorized':
        #     self.toggleCollapsed(None)

    def removeTransaction(self, transaction):
        newTransactions = self.transactions
        newTransactions.remove(transaction)
        self.transactions = []
        self.addTransactions(newTransactions)

    def updateAmtDisplay(self):
        totalAmount = 0
        if len(self.transactions):
            for idx, transaction in enumerate(self.transactions):
                totalAmount += float(transaction.amt)
        if self.name == 'Uncategorized':
            self.uncategorizedAmtDisplay.setText('$' + str(totalAmount))
        else:
            self.progressBar.updateValues(self.categoryTotal, totalAmount)

    def lineContextMenu(self, transactionLine):
        menu = QMenu(self)
        editAction = QAction('Edit Transaction Name')
        # editAction.triggered.connect(lambda evt: self.editTransaction(transactionLine))
        menu.addAction(editAction)
        menu.exec_(QCursor.pos())

    def titleContextMenu(self, event):
        menu = QMenu(self)
        editAction = QAction('Edit Name')
        editAction.triggered.connect(self.promptEditTitle)
        removeAction = QAction('Remove Category')
        removeAction.triggered.connect(self.removeCategory)

        menu.addAction(editAction)
        menu.addAction(removeAction)
        menu.exec_(QCursor.pos())

    def toggleCollapsed(self, event):
        if not event or event.button() == Qt.MouseButton.LeftButton:
            self.collapsed = not self.collapsed
            if self.collapsed:
                self.collapseButton.setText('⊞')
                self.transactionArea.hide()
                self.collapseButton.setToolTip('expand')
            else:
                self.collapseButton.setText('⊟')
                self.transactionArea.show()
                self.collapseButton.setToolTip('collapse')

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            transactionTitle = event.mimeData().text()
            self.state.next(Events.transaction_drop_event, transactionTitle, self.name)

    def removeCategory(self):
        self.state.next(Events.remove_category, self.name, self.transactions)

    def promptEditVal(self, title, currentAmount):
        modal = EditCategoryTotalModal()
        data = modal.getData(currentAmount)
        if data:
            self.state.next(Events.update_category_total, self.name, int(data))
            self.categoryTotal = int(data)
            self.updateAmtDisplay()

    def promptEditTitle(self):
        modal = EditTextModal(self.name, 'Edit Title')
        data = modal.getData()
        if data:
            self.state.next(Events.update_category_title, self.name, data)
            self.name = data
            self.headerText.setText(self.name)